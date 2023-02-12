import pandas as pd
import os
import json
from data import clean_dataset, get_dataset
from tensorflow import keras
from keras.layers import LSTM, Dense, Dropout, TimeDistributed
import plotly.graph_objects as go
import plotly.io as pio


# args = {
#     'exe_name': 'firefox.exe',
#     'lookback': 5,
#     'epochs': 100,
#     'learning_rate': 0.001,
#     'loss': 'mse',
#     'experiment': 1
# }

class LSTM_1:
    def __init__(self, args) -> None:
        self.args = args
        experiment = args['experiment']
        self.dir_path = f'../../../outputs/LSTM_{experiment}'
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)
        with open(f'{self.dir_path}/config.json', 'w') as file:
            json.dump(args, file)
    
    def train(self):
        file_path = "../../../data/processed/lstm_dataset_local.csv"
        print('Processing dataset...')
        df = clean_dataset(file_path)
        self.input_df = df[df['Value'] == self.args['exe_name']].reset_index()
        self.input_df = self.input_df.groupby(pd.Grouper(key='Start', freq='H')).sum().reset_index()
        X, y, self.scaler = get_dataset(self.input_df, self.args['lookback'])

        self.train_size = int(X.shape[0] * 0.8)
        self.X_train, self.X_test = X[:self.train_size, :, :], X[self.train_size:, :, :]
        self.y_train, self.y_test = y[:self.train_size], y[self.train_size:]

        feature_shape = self.X_train.shape[2]

        self.model = keras.Sequential()
        self.model.add(LSTM(32, return_sequences=True, input_shape=(self.args['lookback'], feature_shape)))
        # self.model.add(Dropout(0.2))

        self.model.add(LSTM(32, return_sequences=True))
        # self.model.add(Dropout(0.2))

        self.model.add(LSTM(16, return_sequences=True))
        # self.model.add(Dropout(0.2))

        self.model.add(LSTM(16))
        # self.model.add(Dropout(0.2))

        # self.model.add(TimeDistributed(Dense(1)))
        self.model.add(Dense(32))
        self.model.add(Dense(16))
        self.model.add(Dense(1))
        opt = keras.optimizers.Adam(learning_rate=self.args['learning_rate'])
        self.model.compile(optimizer=opt, loss=self.args['loss'])

        print('Training model...')
        self.history = self.model.fit(self.X_train, self.y_train, epochs=self.args['epochs'], verbose=2)
        print('Finished training.')

        train_loss = self.model.evaluate(self.X_train, self.y_train)
        print(f'Total loss: {train_loss}')

        print('Plotting the loss over epoch')
        loss = self.history.history['loss']
        loss_layout = go.Layout(
            title='Loss plot',
            xaxis={'title':'Epoch'},
            yaxis={'title':'Loss'}
        )
        loss_fig = go.Figure([
            go.Scatter(x=list(range(self.args['epochs'])), y=loss, mode='lines',name = 'training loss')
        ], layout=loss_layout)
        loss_fig.show()

        print('Saving everything...')
        with open(f'{self.dir_path}/train_history.json', 'w') as file:
            json.dump(self.history.history, file)
        self.model.save(f'{self.dir_path}/model.h5')
        pio.write_image(loss_fig, f'{self.dir_path}/loss.png', width=985, height=525)
        print(f'Model, model history, loss plot saved at {self.dir_path}')

    def evaluate(self):
        test_loss = self.model.evaluate(self.X_test, self.y_test)
        print(f'Test loss: {test_loss}')

        print('Plotting the prediction and ground truth')
        train_pred = self.scaler.inverse_transform(self.model.predict(self.X_train, verbose=0))
        test_pred = self.scaler.inverse_transform(self.model.predict(self.X_test, verbose=0))

        pred_layout = go.Layout(
            title='Firefox used in seconds per hour',
        #     xaxis={'title':'Date'},
            yaxis={'title':'Duration(s)'}
        )
        pred_fig = go.Figure([
            go.Scatter(x=self.input_df['Start'], y=self.input_df['Time_diff_sec'].values, name='ground truth'),
            go.Scatter(x=self.input_df['Start'].iloc[:self.train_size], y=train_pred[:,0], name='train prediction'),
            go.Scatter(x=self.input_df['Start'].iloc[self.train_size:], y=test_pred[:,0], name='test prediction')
        ], layout=pred_layout)
        pred_fig.show()

        pio.write_image(pred_fig, f'{self.dir_path}/prediction.png', width=985, height=525)
        print(f'Prediction plot saved at {self.dir_path}')


