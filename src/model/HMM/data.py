import pandas as pd
import math
import random
import os

def clean_data(raw_path, test_data):
    """
    Concatenate raw dataframes with <s> token indicating the start of the collection and save the series of executables into dataframe

    Parameters:
    raw_path (str): path of raw dataframes
    """
    if test_data:
        out_path = raw_path.replace('raw/dataset', 'test/hmm_data.csv')
    else:
        out_path = raw_path.replace('raw/dataset', 'all/hmm_data.csv')
    if os.path.exists(out_path):
        return pd.read_csv(out_path)
    exes = []
    start = pd.Series(['<s>'])
    directory = os.fsencode(raw_path)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"): 
            df = pd.read_csv(f'{raw_path}/{filename}', delimiter='\t')
            df = df[df["ID_INPUT"] == 3][['MEASUREMENT_TIME', 'VALUE']]
            if df.shape[0] > 0:
                start = pd.DataFrame({'MEASUREMENT_TIME': [df.iloc[0,0]], 'VALUE': ['<s>']})
                exes.append(pd.concat([start, df]))
    combined = pd.concat(exes).reset_index(drop=True)
    combined['MEASUREMENT_TIME'] = pd.to_datetime(combined['MEASUREMENT_TIME'])
    combined = combined.sort_values(by='MEASUREMENT_TIME', ascending=True).reset_index(drop=True)
    combined.to_csv(out_path, index=False)
    return combined

def get_dataset(raw_path, test_data):
    """
    Get X and y for model

    Parameters:
    raw_path (str): path of raw dataframes
    """
    df = clean_data(raw_path, test_data)
    df = df['VALUE']
    y = df[1:].copy().reset_index(drop=True)
    X = df[:-1].copy().reset_index(drop=True)
    return X, y

def train_test_split(X, y, test_size=0.2):
    """
    Split X and y in to training and testing set

    Parameters:
    test_size (float): size of test set (in percentage)

    Returns:
    X_train: given executables of training set
    y_train: the ground-truth executable given the executable from X_train
    X_test: given executables of test set
    y_test: the ground-truth executable given the executable from X_test
    """
    X_train = X
    y_train = y
    test_count = math.floor(len(X) * test_size)
    X_test, y_test = zip(*random.sample(list(zip(X, y)), test_count))
    return X_train, y_train, X_test, y_test
