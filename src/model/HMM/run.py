from HMM import HMM
from data import clean_data, get_dataset, train_test_split
import os
import argparse

parser = argparse.ArgumentParser()

# File related
parser.add_argument('--raw_path', default='data/raw', type=str,
                    help='(relative) file path of raw datasets(csv)')
parser.add_argument('--exe_path', default='data/processed/exe.csv', type=str,
                    help='(relative) file path of executable dataset(csv)')  
# Model Related
parser.add_argument('--test_size', default=0.2, type=int,
                    help='Test set size (percentage of entire dataset)')
parser.add_argument('--top', default=1, type=int,
                    help='Number of executables to predict for each data point')

args = vars(parser.parse_args())

def main(args):
    os.chdir('../../..')
    if not os.path.exists(args['exe_path']):
        clean_data(args['raw_path'])
    X, y = get_dataset(args['exe_path'])
    X_train, y_train, X_test, y_test = train_test_split(X, y, args['test_size'])

    model = HMM()
    model.fit(X_train, y_train)
    pred = model.predict(X_test, args['top'])
    accuracy = model.evaluate(pred, y_test)
    print(model.transition_matrix)
    print(accuracy)

if __name__ == "__main__":
    main(args)