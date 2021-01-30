from apihandler import APIHandler
from dbhandler import DBHandler
from modelhandler import ModelHandler

class Helper:
    def __init__(self):
        self.handler = DBHandler()
        self.modelhandler = ModelHandler()

    def resetDB(self):
        self.handler.connect()
        self.handler.reinitAllData()
        self.handler.commit()


def logBuy(symbol, price):
    print(f"Placing order for {symbol} at {price}")
    