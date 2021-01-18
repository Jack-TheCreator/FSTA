import alpaca_trade_api as tradeapi
import key

class APIHandler:
    def __init__(self):
        self.api = tradeapi.REST(key.key, key.secret, base_url=key.endpoint)

    def getStocks(self) -> list:
        return(self.api.list_assets())

    def getPricesByDay(self, stock_symbols:list):
        return(self.api.get_barset(stock_symbols,'day'))

    def getPricesByMinute(self, stock_symbols:list):
        return(self.api.get_barset(stock_symbols,'minute'))