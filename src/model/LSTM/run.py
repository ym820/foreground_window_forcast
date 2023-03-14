import argparse
from LSTM import LSTM_1

parser = argparse.ArgumentParser()

# File related
parser.add_argument('-exe', '--exe_name', default='firefox.exe', type=str,
                    help='The executable name to predict')
parser.add_argument('-lb', '--lookback', default=5, type=int,
                    help='Lookback window (hyper-parameter) for dataset processing')  
# Model Related
parser.add_argument('-e', '--epochs', default=100, type=int,
                    help='Number of epochs')
parser.add_argument('-lr', '--learning_rate', default=0.001, type=float,
                    help='Learning rate')
parser.add_argument('-l', '--loss', default='mse', type=str,
                    help='Loss function')
parser.add_argument('-ex', '--experiment', default=1, type=int,
                    help='Experiment no.')
parser.add_argument('-s', '--shuffle', default=False, type=bool,
                    help='Whether to shuffle for train test split')

args = vars(parser.parse_args())

def main(args):
    model = LSTM_1(args)
    model.train()
    # model.evaluate()

if __name__ == "__main__":
    main(args)