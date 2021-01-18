import sqlite3
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from dbhandler import DBHandler
from modelhandler import ModelHandler

app = FastAPI()
templates = Jinja2Templates(directory="templates")
dbhandler = DBHandler()
modelhandler = ModelHandler()


@app.get("/")
def index(request: Request):
    dbhandler.connect()    
    rows = dbhandler.getAllStocks()
    return templates.TemplateResponse("index.html", {"request":request,"stocks":rows})

@app.get("/stock/{symbol}")
def stock_view(request:Request, symbol):
    dbhandler.connect()
    prices = dbhandler.getPricesBySymbol(symbol)
    row = dbhandler.getStockbySymbol(symbol)
    print(row)
    return templates.TemplateResponse("stock_view.html", {"request":request, "stock":row, "prices":prices})

@app.get("/model/{symbol}")
def model_view(request:Request, symbol):
    modelpred = modelhandler.getModelPred(symbol)
    return "Model"