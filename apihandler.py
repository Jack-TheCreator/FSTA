import alpaca_trade_api as tradeapi
import key
from datetime import date
import pandas as pd
from alpha_vantage.timeseries import TimeSeries

class APIHandler:
    def __init__(self):
        self.api = tradeapi.REST(key.key, key.secret, base_url=key.endpoint)
        self.currentDate = date.today().isoformat()

    def getStocks(self) -> list:
        return(self.api.list_assets())

    def getPricesByDay(self, stock_symbols:list):
        return(self.api.get_barset(stock_symbols,'day'))

    def getPricesByMinute(self, stock_symbols:list):
        return(self.api.get_barset(stock_symbols,'minute'))

    #more acurate miniute data but with limited calls
    def getPolygonPriceByMinute(self, symbol):
        return(self.api.polygon.historic_agg_v2(symbol, 1, 'minute', _from='2021-01-29', to='2021-01-29').df)
 
    #testing new api
    def getPricesBy15Minutes(self, symbol):
        ts = TimeSeries(key=key.key2,output_format="pandas")
        minBars, metaData = ts.get_intraday(symbol=symbol,interval="1min",outputsize="full")
        return(minBars, metaData)

    def getOrders(self):
        return(self.api.list_orders(status='all',limit=500,after=f"{self.currentDate}T13:30:00Z"))

    def placeBuy(self, symbol,limit_price,pricerange):
        self.api.submit_order(
            symbol=symbol,
            side='buy',
            type='limit',
            qty='100',
            time_in_force='day',
            order_class='bracket',
            limit_price = limit_price,
            take_profit=dict(
                limit_price=limit_price+pricerange,
            ),
            stop_loss=dict(
                stop_price=limit_price-pricerange,
            )
        )
