from apihandler import APIHandler
from dbhandler import DBHandler

handler = DBHandler()
handler.connect()
handler.reinitAllData()
handler.commit()
