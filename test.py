from apihandler import APIHandler
from dbhandler import DBHandler

handler = DBHandler()

print(handler.getPricesBySymbol('AAPL'))
