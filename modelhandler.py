import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.metrics import mean_squared_error
from keras import models
from keras.preprocessing.sequence import TimeseriesGenerator
from dbhandler import DBHandler
import pandas as pd

class Model:
    def __init__(self, df, train_size=0.8):
        self.df = df
        self.predictAhead = 5
        self.time_steps = 1
        self.train_size = int(len(df)*train_size)

    def buildModel(self, symbol):
        nuerons = [10, 15, 20 ,25]
        num_epochs = [100, 250, 500, 1000]
        reps = 1

        close = self.df['close'].values
        train, test = close[:self.train_size], close[self.train_size:]
        train = np.reshape(train, (-1,1))
        test = np.reshape(test, (-1,1))

        trainData = TimeseriesGenerator(train, train, length=self.time_steps, batch_size=20)
        testData = TimeseriesGenerator(test, test, length=self.time_steps, batch_size=1)

        results = {}

        testVals = test[self.time_steps:]
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
                    print(mean)
                    results[mean[0]] = model

        bestModel = results[min(results.keys())]
        bestModel.save(symbol)

    def getPredictions(self,symbol):
        values = self.df['close'].values
        model = load_model(symbol)
        # --------Predictions------------#
        values = values.reshape(-1)
        predictions = values[-self.time_steps:]
        for derp in range(self.predictAhead):
            x = predictions[-self.time_steps:]
            x = x.reshape((1, self.time_steps, 1))
            out = model.predict(x)[0][0]
            predictions = np.append(predictions, out)
        predictions = predictions[self.time_steps:]
        # --------------------------------#
        predictions = np.asarray(predictions)
        self.pred = np.reshape(predictions, (-1, 1))
        return(self.pred)
    

class ModelHandler:
    def __init__(self):
        self.handler = DBHandler()

    def createModel(self, symbol:str):
        self.handler.connect()
        prices = self.handler.getDayPricesBySymbol(symbol)
        pd_frame = self.pandify(prices)
        self.model = Model(pd_frame)
        self.model.buildModel(symbol)

    def getModelPred(self, symbol:str):
        self.handler.connect()
        prices = self.handler.getDayPricesBySymbol(symbol)
        pd_frame = self.pandify(prices)
        self.model = Model(pd_frame)
        print(self.model.getPredictions(symbol))

    def pandify(self, prices:list):
        return(pd.DataFrame(prices, columns=["symbol","Date","open","high","low","close"]))
        

