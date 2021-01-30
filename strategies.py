
import helper
from apihandler import APIHandler
from dbhandler import DBHandler
import pandas as pd
from datetime import date

class Strategies:
    def __init__(self):
        self.handler = DBHandler()
        self.help = helper.Helper()
        self.apihandler = APIHandler()
        self.current_date = date.today().isoformat()

    def openingRangeBreakout(self):
        self.handler.connect()
        #should probably get strategyID dynamically but you know...
        stocks = self.handler.getStocksByStrategyID(1)
        
        #get orders and check if one made for stock
        orders = self.apihandler.getOrders()
        syms = []
        for order in orders:
            syms.append(order.symbol)

        
        start_minute_bar = f"{self.current_date} 09:30:00-04:00"
        end_minute_bar = f"{self.current_date} 09:45:00-04:00"
        symbols = []
        for stock in stocks:
            symbols.append(stock[0])
        
        for symbol in symbols:
            print(symbol)
            minBars = self.apihandler.getPolygonPriceByMinute(symbol)
            if(not minBars.empty):
                print(minBars)
                minBars.columns = ['open', 'high', 'low', 'close', 'volume','vwap']
                opening_range_mask = (minBars.index >= start_minute_bar) & (minBars.index < end_minute_bar)
                opening_range_bars = minBars.loc[opening_range_mask]
                opening_range_low = opening_range_bars['low'].min()
                opening_range_high = opening_range_bars['high'].max()
                open_range = opening_range_high-opening_range_low
                after_opening_range_mask = minBars.index >= end_minute_bar
                after_opening_range_bars = minBars.loc[after_opening_range_mask]
                after_opening_range_breakout = after_opening_range_bars[after_opening_range_bars['close'] > opening_range_high]
                
                if(not after_opening_range_breakout.empty):
                    if(symbol in syms):
                        limit_price = after_opening_range_breakout.iloc[0]['close']
                        helper.logBuy(symbol,limit_price)
                        self.apihandler.placeBuy(symbol, limit_price, open_range)
            else:
                print(f"can't retrieve data for {symbol}")

    def modelStrat(self):
        raise NotImplementedError