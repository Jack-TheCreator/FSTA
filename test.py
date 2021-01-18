from apihandler import APIHandler
from dbhandler import DBHandler

handler = DBHandler()

handler.connect()
handler.repopAllStocks()
handler.repopDayPrice()
handler.commit()
