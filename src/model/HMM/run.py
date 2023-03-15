from HMM import HMM
from visualize import visualize
from data import clean_data, get_dataset, train_test_split
import os
import argparse
import json

parser = argparse.ArgumentParser()
 
# Model Related
parser.add_argument('-td', '--test_data', default=False, type=bool,
                    help='Whether use test data')
parser.add_argument('-ts', '--test_size', default=0.2, type=int,
                    help='Test set size (percentage of entire dataset)')
parser.add_argument('-t', '--top', default=1, type=int,
                    help='Number of executables to predict for each data point')
parser.add_argument('-ex', '--experiment', default=1, type=int,
                    help='Experiment no.')

args = vars(parser.parse_args())

def main(args):
    experiment = args['experiment']
    dir_path = f'../../../outputs/HMM_expt_{experiment}'
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    with open(f'{dir_path}/config.json', 'w') as file:
        json.dump(args, file)

    raw_path = '../../../data/raw/dataset'
    X, y = get_dataset(raw_path, args['test_data'])
    X_train, y_train, X_test, y_test = train_test_split(X, y, args['test_size'])

    model = HMM()
    model.fit(X_train, y_train)
    pred = model.predict(X_test, args['top'])
    accuracy = model.evaluate(pred, y_test)
    outputs = {
        'accuracy': accuracy
    }
    with open(f'{dir_path}/transition_matrix.json', 'w') as file:
        json.dump(model.transition_matrix, file)
    with open(f'{dir_path}/output.json', 'w') as file:
        json.dump(outputs, file)
    
    visualize(model, dir_path)

if __name__ == "__main__":
    main(args)