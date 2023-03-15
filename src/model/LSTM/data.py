import pandas as pd
import os
import numpy as np
import datetime
import sqlite3 as sql
import csv
from sqlite3 import Error
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, MinMaxScaler

def export_dbs_as_csv():
    input_folder = '../../../data/raw/database'
    output_folder = '../../../data/raw/dataset'
    for db in os.listdir(input_folder):
        new_name = db.strip(".db") + ".csv"
        try:
            input_file_path = os.path.join(input_folder, db)
            conn=sql.connect(input_file_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM COUNTERS_STRING_TIME_DATA")
            print("Exporting data into CSV............")
            dirpath = os.path.join(output_folder, new_name)
            with open(dirpath, "w") as csv_file:
                csv_writer = csv.writer(csv_file, delimiter="\t")
                csv_writer.writerow([i[0] for i in cursor.description])
                csv_writer.writerows(cursor)
            print("Data exported Successfully into {}".format(dirpath))

        except Error as e:
            print(e)

        # Close database connection
        finally:
            conn.close()
    return

def combine_dataset(raw_path):
    """
    Concatenate raw dataframes with <s> token indicating the start of the collection and save the series of executables into dataframe

    Parameters:
    raw_path (str): path of raw dataframes
    """
    datasets = []
    directory = os.fsencode(raw_path)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"):
            df = pd.read_csv(f'{raw_path}/{filename}', delimiter='\t')
            if df.shape[0] > 0:
                temp = df[df['ID_INPUT'] == 3][['MEASUREMENT_TIME', 'VALUE']].reset_index(drop=True)
                temp = temp.rename(columns={'MEASUREMENT_TIME': 'Start', 'VALUE': 'Value'})
                temp['Start'] = pd.to_datetime(temp['Start']).dt.tz_localize(tz='GMT+0').dt.tz_convert('America/Los_Angeles').dt.tz_localize(None)
                temp['End'] = temp['Start'].shift(-1)
                temp['Duration'] = (temp['Start'].shift(-1) - temp['Start'])
                temp = temp.drop(len(temp)-1)
                datasets.append(temp)
    output_dataset = pd.concat(datasets).sort_values(by='Start').reset_index(drop=True)
    output_dataset.to_csv('../../../data/all/lstm_data_local.csv', index=False)
    return output_dataset

def row_helper(row):
    delta = datetime.timedelta(hours=1)
    if row['Time_diff_sec'] < row['sec_to_next_hr']:
        row['End'] = row['Start'] + pd.to_timedelta(row['Time_diff_sec'], unit='S')
        return [row]
    row2 = row.copy()
    
    row['End'] = (row['Start']+delta).floor('H')
    row2['Start'] = row['End']
    row2['End'] = (row['End']+delta).floor('H')
    
    row2['Time_diff_sec'] = row['Time_diff_sec'] - row['sec_to_next_hr']
    row2['sec_to_next_hr'] = 3600
    row['Time_diff_sec'] = row['sec_to_next_hr']
    return [row] + row_helper(row2)

def clean_row(row):
    if row['Time_diff_sec'] > row['sec_to_next_hr']:
        return pd.DataFrame(row_helper(row))
    return pd.DataFrame([row])

def clean_dataset(file_path):
    df = pd.read_csv(file_path, parse_dates=['Start', 'End'])
    df['Duration'] = df['Duration'].apply(lambda x: pd.Timedelta(x))
    df['Time_diff_sec'] = df['Duration'].apply(lambda x: x.total_seconds())
    df = df.drop(columns='Duration')
    delta = datetime.timedelta(hours=1)
    df['sec_to_next_hr'] = df['Start'].apply(lambda x: ((x+delta).replace(microsecond=0, second=0, minute=0) - x).seconds)

    return pd.concat([clean_row(row) for _, row in df.iterrows()], ignore_index=True)
  
def transformation(column, max_value):
  sin_values = [np.sin((2*np.pi*x)/max_value) for x in list(column)]
  cos_values = [np.cos((2*np.pi*x)/max_value) for x in list(column)]
  return sin_values, cos_values

def process(temp):
    temp['dayofweek'] = temp['Start'].apply(lambda x: x.dayofweek).astype('category')
    temp['dayofmonth'] = temp['Start'].apply(lambda x: x.day).astype('category')
    temp['dayofyear'] = temp['Start'].apply(lambda x: x.dayofyear).astype('category')
    temp['hour'] = temp['Start'].apply(lambda x: x.hour).astype('category')
    temp['month'] = temp['Start'].apply(lambda x: x.month).astype('category')
    temp['is_weekend'] = temp['Start'].apply(lambda x: 1 if x == 5 or x == 6 else -1)
    temp['is_winter_holiday'] = temp['Start'].apply(lambda x: 1 if x > datetime.datetime(2022, 12, 12) or x < datetime.datetime(2023, 1, 8) else -1)
    temp = temp.drop(columns='Start')
    data = pd.get_dummies(temp, columns=['dayofweek', 'dayofmonth', 'dayofyear', 'hour','minute','month']).values

    return data

def get_dataset(df, args):
    temp = df.copy()
    temp['minute'] = temp['Start'].apply(lambda x: x.minute)
    temp = temp.groupby(pd.Grouper(key='Start', freq='H')).agg({
            'Time_diff_sec': 'sum',
            'minute': 'min'
        }).reset_index().fillna(0)
    temp = temp[(temp['Start'] < '2022-12-23') | (temp['Start'] > '2023-01-08')]

    scaler = MinMaxScaler()
    scaler.fit(temp[['Time_diff_sec']])
    temp[['Time_diff_sec']] = scaler.transform(temp[['Time_diff_sec']])

    data = process(temp)
    
    X, y = [], []
    for i in range(len(data)-args['lookback']):
        # gather input and output parts of the pattern
        seq_x, seq_y = data[i:i+args['lookback'], :], data[i+args['lookback'], 0:1]
        X.append(seq_x)
        y.append(seq_y)
    
    X, y = np.array(X), np.array(y)
    test_size = int(X.shape[0] * args['test_size'])
    if args['random']:
        start = np.random.randint(0, X.shape[0]-test_size)
        end = start + test_size
    else:
        start = X.shape[0] - test_size
        end = X.shape[0]
    test_ind = np.zeros(X.shape[0], dtype=bool)
    test_ind[start:end] = True
    X_train, X_test = X[~test_ind, :, :], X[test_ind, :, :]
    y_train, y_test = y[~test_ind], y[test_ind]
    return X_train, y_train, X_test, y_test, scaler, start, end