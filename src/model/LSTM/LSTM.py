import pandas as pd
import os
import json
import numpy as np
from data import clean_dataset, get_dataset
from tensorflow import keras
from keras.layers import LSTM, Dense, Bidirectional
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio


class LSTM_1:
    def __init__(self, args) -> None:
        self.args = args
        experiment = args['experiment']
        self.dir_path = f'../../../outputs/LSTM_{experiment}'
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)
        with open(f'{self.dir_path}/config.json', 'w') as file:
            json.dump(args, file)

    def train_model(self):
        feature_shape = self.X_train.shape[2]

        self.model = keras.Sequential()
        self.model.add(LSTM(32, return_sequences=True, input_shape=(self.args['lookback'], feature_shape)))

        self.model.add(LSTM(16, return_sequences=True))

        self.model.add(LSTM(16))

        self.model.add(Dense(32))
        self.model.add(Dense(16))
        self.model.add(Dense(1, activation='sigmoid'))
        opt = keras.optimizers.Adam(learning_rate=self.args['learning_rate'])
        self.model.compile(optimizer=opt, loss=self.args['loss'])

        print('======== TRAIN ========')
        self.history = self.model.fit(self.X_train, self.y_train, epochs=self.args['epochs'], verbose=2)

    def train(self):
        file_path = "../../../data/processed/lstm_data_local.csv"
        print('======== PROCESS DATASET ========')
        self.df = clean_dataset(file_path)
        self.df = self.df[self.df['Value'] == self.args['exe_name']].reset_index()
        self.X_train, self.y_train, self.X_test, self.y_test, self.scaler, self.start, self.end = get_dataset(self.df, self.args)
        print('Finished data processing')

        self.train_model()

        self.train_pred = self.scaler.inverse_transform(self.model.predict(self.X_train, verbose=0))
        self.test_pred = self.scaler.inverse_transform(self.model.predict(self.X_test, verbose=0))

        print('======== EVALUATE ========')
        self.plot_loss()
        self.plot_prediction()
        self.evaluate()

        print('======== SAVE MODEL ========')
        with open(f'{self.dir_path}/train_history.json', 'w') as file:
            json.dump(self.history.history, file)
        self.model.save(f'{self.dir_path}/model.h5')
        print('Model and model history saved')
        print(f'Finished. Everything is saved at {self.dir_path}')

    def get_accuracy(self, pred, target, bound=10):
        return np.mean(np.abs(pred - target) < bound)

    def get_nonzero_accuracy(self, pred, target, bound=10):
        ind = np.where(target!=0)[0]
        return np.mean(np.abs(pred[ind] - target[ind]) < bound)
    
    def evaluate(self):
        print('Printing evaluation metrics:')
        results = {}
        results['train_loss'] = self.model.evaluate(self.X_train, self.y_train, verbose=0)
        results['train_acc_5'] = self.get_accuracy(self.train_pred, self.y_train, 5)
        results['train_acc_10'] = self.get_accuracy(self.train_pred, self.y_train, 10)
        results['train_acc_60'] = self.get_accuracy(self.train_pred, self.y_train, 60)
        results['nonzero_train_acc_5'] = self.get_nonzero_accuracy(self.train_pred, self.y_train, 5)
        results['nonzero_train_acc_10'] = self.get_nonzero_accuracy(self.train_pred, self.y_train, 10)
        results['nonzero_train_acc_60'] = self.get_nonzero_accuracy(self.train_pred, self.y_train, 60)
        results['test_loss'] = self.model.evaluate(self.X_test, self.y_test, verbose=0)
        results['test_acc_5'] = self.get_accuracy(self.test_pred, self.y_test, 5)
        results['test_acc_10'] = self.get_accuracy(self.test_pred, self.y_test, 10)
        results['test_acc_60'] = self.get_accuracy(self.test_pred, self.y_test, 60)    
        results['nonzero_test_acc_5'] = self.get_nonzero_accuracy(self.test_pred, self.y_test, 5)
        results['nonzero_test_acc_10'] = self.get_nonzero_accuracy(self.test_pred, self.y_test, 10)
        results['nonzero_test_acc_60'] = self.get_nonzero_accuracy(self.test_pred, self.y_test, 60)

        print("""Train Loss: {train_loss}
Train Accuracy (abs diff within 5s): {train_acc_5}
Train Accuracy (abs diff within 10s): {train_acc_10}
Train Accuracy (abs diff within 60s): {train_acc_60}
Non-zero Train Accuracy (abs diff within 5s): {nonzero_train_acc_5}
Non-zero Train Accuracy (abs diff within 10s): {nonzero_train_acc_10}
Non-zero Train Accuracy (abs diff within 60s): {nonzero_train_acc_60}
Test Loss: {test_loss}
Test Accuracy (abs diff within 5s): {test_acc_5}
Test Accuracy (abs diff within 10s): {test_acc_10}
Test Accuracy (abs diff within 60s): {test_acc_60}
Non-zero Test Accuracy (abs diff within 5s): {nonzero_test_acc_5}
Non-zero Test Accuracy (abs diff within 10s): {nonzero_test_acc_10}
Non-zero Test Accuracy (abs diff within 60s): {nonzero_test_acc_60}""".format(**results))
        
        with open(f'{self.dir_path}/results.json', 'w') as file:
            json.dump(results, file)

    def plot_loss(self):
            loss = self.history.history['loss']
            layout = go.Layout(
                xaxis={'title':'Epoch'},
                yaxis={'title':'Loss'}
            )
            fig = go.Figure([go.Scatter(x=list(range(self.args['epochs'])), y=loss, mode='lines',name = 'Training Loss')], layout=layout)
            pio.write_html(fig, f'{self.dir_path}/loss.html')
            pio.write_image(fig, f'{self.dir_path}/loss.png', width=1200, height=500)
            print('Loss plot saved')

    def plot_prediction(self):
            fig = make_subplots(rows=2, cols=1, subplot_titles=['Prediction and Ground Truth', "Training Loss"])
            layout = go.Layout(
                title='Firefox used in seconds per hour',
            #     xaxis={'title':'Date'},
                yaxis={'title':'Duration(s)'}
            )
            temp = self.df.groupby(pd.Grouper(key='Start', freq='H'))['Time_diff_sec'].sum().reset_index()
            temp = temp[(temp['Start'] < '2022-12-23') | (temp['Start'] > '2023-01-08')]
            temp = temp.iloc[self.args['lookback']:, :]
            dates = temp['Start'].values
            fig = go.Figure([
                go.Scatter(x=dates, y=temp['Time_diff_sec'].iloc[:].values, name='data'),
                go.Scatter(x=dates[:self.start], y=self.train_pred[:self.start,0], line=dict(color='red'),name='train prediction'),
                go.Scatter(x=dates[self.end:], y=self.train_pred[self.start:,0], line=dict(color='red'),name='train prediction', showlegend=False),
                go.Scatter(x=dates[self.start:self.end], y=self.test_pred[:,0], line=dict(color='#00CC96'),name='test prediction')
            ], layout=layout)
            fig.update_xaxes(
            rangebreaks=[dict(values=pd.date_range('2022-12-23', '2023-01-08'))] # hide dates with no values
        )
            pio.write_html(fig, f'{self.dir_path}/prediction.html')
            pio.write_image(fig, f'{self.dir_path}/prediction.png', width=1200, height=500)
            print('Prediction plot saved')


