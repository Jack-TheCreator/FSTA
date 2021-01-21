from apihandler import APIHandler
from dbhandler import DBHandler
from modelhandler import ModelHandler

handler = DBHandler()
handler.connect()
handler.repopStrategies()
handler.commit()