import pandas as pd
import math
import random
import os

def clean_data(raw_path, file_path):
    """
    Concatenate raw dataframes with <s> token indicating the start of the collection and save the series of executables into dataframe

    Parameters:
    raw_path (str): path of raw dataframes
    """
    if os.path.isfile(file_path):
        return pd.read_csv(file_path)
    exes = []
    start = pd.Series(['<s>'])
    for i in range(1, 30):
        if i == 28:
            continue
        file_path = f"{raw_path}/df{i}.csv"
        df = pd.read_csv(file_path)
        df = df[df["ID_INPUT"] == 3]
        exes.append(pd.concat([start, df.VALUE]))
    output_exe = pd.concat(exes).reset_index(drop=True)
    output_exe.to_csv(file_path, index=False)
    return output_exe

def get_dataset(exe_path):
    """
    Get X and y for model

    Parameters:
    exe_path (str): path of executable dataframe
    """
    exe = pd.read_csv(exe_path)['0']
    y = exe[1:].copy().reset_index(drop=True)
    X = exe[:-1].copy().reset_index(drop=True)
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
