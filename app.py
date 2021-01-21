import sqlite3
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from dbhandler import DBHandler
from modelhandler import ModelHandler
from fastapi.staticfiles import StaticFiles
import json
from datetime import datetime



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
dbhandler = DBHandler()
modelhandler = ModelHandler()
#cursym used for selecting minute data
#I know theres a better way but it works
cursym = ""

@app.get("/")
def index(request: Request):
    stockFilter = request.query_params.get('filter', False)
    dbhandler.connect()
    if(stockFilter=='new_intraday_highs'):
        pass
    elif(stockFilter=='new_intraday_low'):
        pass
    elif(stockFilter=='new_closing_highs'):
        rows = dbhandler.getClosingHigh()
    elif(stockFilter=='new_closing_low'):
        pass
    else:
        rows = dbhandler.getAllStocks()
    print(rows)
    return templates.TemplateResponse("index.html", {"request":request,"stocks":rows})

@app.get("/stock/{symbol}")
def stock_view(request:Request, symbol):
    dbhandler.connect()
    prices = dbhandler.getDayPricesBySymbol(symbol)
    row = dbhandler.getStockbySymbol(symbol)
    strats = dbhandler.getStrategies()
    return templates.TemplateResponse("stock_view.html", {"request":request, "stock":row, "prices":prices, "strats":strats})

@app.get("/model/{symbol}")
def model_view(request:Request, symbol):
    return "Too Be Implemented"

@app.get("/minute/{symbol}")
def minute_view(request:Request, symbol):
    global cursym
    dbhandler.connect()
    cursym = symbol
    prices = dbhandler.getMinutePriceBySymbol(symbol)
    row = dbhandler.getStockbySymbol(symbol)
    return templates.TemplateResponse("stock_minute_view.html", {"request":request, "stock":row, "prices":prices})

@app.get("/minData")
def minData():
    dbhandler.connect()
    prices = dbhandler.getMinutePriceBySymbol(cursym)
    candlesticks = []
    for price in prices:
        date = datetime.today().strftime('%Y-%m-%d')
        dt = date+" "+price[1]
        dt_obj = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
        
       #bug in this timestamp will be fixed!...when i can be bothered
        
        stick = {
            "time":dt_obj.timestamp()*1000,
            "open":price[2],
            "high":price[3],
            "low":price[4],
            "close":price[5]
        }
        candlesticks.append(stick)

    return(candlesticks)
