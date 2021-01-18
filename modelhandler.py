from dbhandler import DBHandler
import pandas as pd

class ModelHandler:
    def __init__(self):
        self.handler = DBHandler()

    def getModelPred(self, symbol:str):
        self.handler.connect()
        prices = self.handler.getPricesBySymbol(symbol)
        pd_frame = self.pandify(prices)
        

    def pandify(self, prices:list):
        return(pd.DataFrame(prices, columns=["symbol","date","open","high","low","close"]))
        

