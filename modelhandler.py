import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras import models
from keras.preprocessing.sequence import TimeseriesGenerator
from dbhandler import DBHandler
import pandas as pd

class Model:
    def __init__(self, df, train_size=0.8):
        self.df = df
        self.scaler = MinMaxScaler()
        self.df[['close']] = self.scaler.fit_transform(self.df[['close']])
        self.predictAhead = 5
        self.time_steps = 1
        self.train_size = int(len(df)*train_size)

    def buildModel(self):
        nuerons = [10, 15, 20 ,25]
        num_epochs = [100, 250, 500, 1000]
        reps = 5

        close = self.df['close'].values
        train, test = close[:self.train_size], close[self.train_size:]
        train = np.reshape(train, (-1,1))
        test = np.reshape(test, (-1,1))

        trainData = TimeseriesGenerator(train, train, length=self.time_steps, batch_size=20)
        testData = TimeseriesGenerator(test, test, length=self.time_steps, batch_size=1)

        results = {}

        testVals = self.scaler.inverse_transform(test[self.time_steps:])
        for _ in range(reps):

            for n in nuerons:

                for e in num_epochs:
                    #######init Model##########
                    model = Sequential()
                    model.add(
                        LSTM(n,
                             activation='relu',
                             input_shape=(self.time_steps, 1))
                    )
                    model.add(Dense(1))
                    model.compile(optimizer='adam', loss='mse')
                    model.fit(trainData, epochs=e, verbose=1)
                    ###########################

                    pred = model.predict_generator(testData)
                    squared = []
                    for p, t in zip(pred, testVals):
                        squared.append((t - p) ** 2)
                    mean = sum(squared) / len(squared)

                    results[mean[0]] = model

        bestModel = results[min(results.keys())]
        bestModel.save("model")

    
        

class ModelHandler:
    def __init__(self):
        self.handler = DBHandler()

    def getModelPred(self, symbol:str):
        self.handler.connect()
        prices = self.handler.getDayPricesBySymbol(symbol)
        pd_frame = self.pandify(prices)
        self.model = Model(pd_frame)
        self.model.buildModel()
        

    def pandify(self, prices:list):
        return(pd.DataFrame(prices, columns=["symbol","Date","open","high","low","close"]))
        

