import sqlite3
import alpaca_trade_api as tradeapi
from apihandler import APIHandler
from datetime import datetime

class DBHandler:    
    def connect(self):
        self.connection = sqlite3.connect('app.db')
        self.cursor = self.connection.cursor()
        self.handler = APIHandler()
        self.connection.row_factory = sqlite3.Row

    def reinitAllData(self):
        self.deleteAllTables()
        self.createTables()
        self.repopAllStocks()
        self.repopDayPrice()
        self.repopMinutePrice()
        print('done')

    def deleteAllTables(self):
        self.cursor.execute("""
            DROP TABLE stock;
        """)
        self.cursor.execute("""
            DROP TABLE stock_price;
        """)
        self.cursor.execute("""
            DROP TABLE stock_minute_price;
        """)

    def createTables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock(
                id INTEGER PRIMARY KEY,
                symbol TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                exchange TEXT NOT NULL
            );
        """)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_price(
                id INTEGER PRIMARY KEY,
                stock_id INTEGER,
                date NOT NULL,
                open NOT NULL,
                high NOT NULL,
                low NOT NULL,
                close NOT NULL,
                volume NOT NULL,
                FOREIGN KEY (stock_id) REFERENCES stock (id)
            );'''
        )
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_minute_price(
                id INTEGER PRIMARY KEY,
                stock_id INTEGER,
                time NOT NULL,
                open NOT NULL,
                high NOT NULL,
                low NOT NULL,
                close NOT NULL,
                volume NOT NULL,
                FOREIGN KEY (stock_id) REFERENCES stock (id)
            );
        """)  

    def repopAllStocks(self):
        stocks = self.handler.getStocks()
        for stock in stocks:
            try:
                if(stock.status == "active" and stock.tradable):
                    self.cursor.execute("INSERT OR IGNORE INTO stock (symbol, name, exchange) VALUES (?,?,?)", (stock.symbol, stock.name, stock.exchange))
            except Exception as e:
                print(e)

    def repopDayPrice(self):
        self.cursor.execute("SELECT id, symbol FROM stock")
        stocks = self.cursor.fetchall()
        stock_dict = {}
        stock_symbols = []
        for stock in stocks:
            stock_symbols.append(stock[1])
            stock_dict[stock[1]]=stock[0]
        for i in range(0, len(stock_symbols), 200):
            chunk = stock_symbols[i:i+200]
            barset = self.handler.getPricesByDay(chunk)
            for symbol in barset:
                for bar in barset[symbol]:
                    stock_id = stock_dict[symbol]
                    self.cursor.execute("""
                        INSERT INTO stock_price (stock_id, date, open, high, low, close, volume)
                        VALUES (?,?,?,?,?,?,?)
                    """,(stock_id,bar.t.date(),bar.o,bar.h,bar.l,bar.c,bar.v))
    
    def repopMinutePrice(self):
        self.cursor.execute("SELECT id, symbol FROM stock")
        stocks = self.cursor.fetchall()
        stock_dict = {}
        stock_symbols = []
        for stock in stocks:
            stock_symbols.append(stock[1])
            stock_dict[stock[1]]=stock[0]
        for i in range(0, len(stock_symbols),200):
            chunk = stock_symbols[i:i+200]
            barset = self.handler.getPricesByMinute(chunk)
            for symbol in barset:
                for bar in barset[symbol]:
                    stock_id = stock_dict[symbol]
                    self.cursor.execute("""
                        INSERT INTO stock_minute_price (stock_id, time, open, high, low, close, volume)
                        VALUES (?,?,?,?,?,?,?)
                    """, (stock_id,str(bar.t.time()),bar.o,bar.h,bar.l,bar.c,bar.v))
            

    def getDayPricesBySymbol(self, symbol:str):
        self.cursor.execute("""
            SELECT symbol, date, open, high, low, close
            FROM stock_price
            JOIN stock on stock.id = stock_price.stock_id
            WHERE symbol = ?
            ORDER BY date DESC;
        """,(symbol,))
        return(self.cursor.fetchall())

    def getMinutePriceBySymbol(self, symbol:str):
        self.cursor.execute("""
            SELECT symbol, time, open, high, low, close
            FROM stock_minute_price
            JOIN stock on stock.id = stock_minute_price.stock_id
            WHERE symbol = ?
            ORDER BY time;
        """,(symbol,))
        return(self.cursor.fetchall())

    def getAllPrices(self):
        self.cursor.execute("""
            SELECT * FROM stock_price
        """)
        return(self.cursor.fetchall())

    def getAllStocks(self):
        self.cursor.execute("""
            SELECT id, symbol, name FROM stock;
        """)
        return(self.cursor.fetchall())

    def getStockbySymbol(self, symbol:str):
        self.cursor.execute("""
        SELECT * FROM stock WHERE symbol = ?;
        """,(symbol,))
        return(self.cursor.fetchone())

    def commit(self):
        self.connection.commit()
