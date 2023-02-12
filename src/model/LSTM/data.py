import pandas as pd
import os
import numpy as np
import datetime
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, MinMaxScaler


def combine_dataset(raw_path, file_path):
    """
    Concatenate raw dataframes with <s> token indicating the start of the collection and save the series of executables into dataframe

    Parameters:
    raw_path (str): path of raw dataframes
    """
    if os.path.isfile(file_path):
        return pd.read_csv(file_path)
    datasets = []
    # start = pd.Series(['<s>'])
    for i in range(1, 30):
        if i == 28:
            continue
        file_path = f"{raw_path}/df{i}.csv"
        df = pd.read_csv(file_path)
        temp = df[df['ID_INPUT'] == 3][['MEASUREMENT_TIME', 'VALUE']].reset_index(drop=True)
        temp = temp.rename(columns={'MEASUREMENT_TIME': 'Start', 'VALUE': 'Value'})
        temp['Start'] = pd.to_datetime(temp['Start']).dt.tz_localize(tz='GMT+0').dt.tz_convert('America/Los_Angeles').dt.tz_localize(None)
        temp['End'] = temp['Start'].shift(-1)
        temp['Duration'] = (temp['Start'].shift(-1) - temp['Start'])
        temp = temp.drop(len(temp)-1)
        datasets.append(temp)
    output_dataset = pd.concat(datasets).reset_index(drop=True)
    # print(output_dataset['Duration'].dtype)
    output_dataset.to_csv(file_path, index=False)
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

def get_dataset(df, lookback):
    # temp = df.groupby(pd.Grouper(key='Start', freq='H')).sum().reset_index()
    df['weekday'] = df['Start'].apply(lambda x: x.dayofweek)#.astype('category')
    df['hour'] = df['Start'].apply(lambda x: x.hour)#.astype('category')
    df['minute'] = df['Start'].apply(lambda x: x.minute)
    df['date'] = df['Start'].apply(lambda x: x.day)
    df['month'] = df['Start'].apply(lambda x: x.month)
    df = df.drop(columns='Start')
#     df = pd.get_dummies(df).values
    df = df.values
    
    X, y = [], []
    for i in range(len(df)-lookback-1):
        # gather input and output parts of the pattern
        seq_x, seq_y = df[i:i+lookback, 1:], df[i+lookback-1, 0:1]
        X.append(seq_x)
        y.append(seq_y)
    scaler = MinMaxScaler()
    scaler.fit(y)
    y = scaler.transform(y)
    return np.array(X), np.array(y), scaler