import sqlite3
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from dbhandler import DBHandler

app = FastAPI()
templates = Jinja2Templates(directory="templates")
handler = DBHandler()


@app.get("/")
def index(request: Request):
    handler.connect()    
    rows = handler.getAllStocks()
    return templates.TemplateResponse("index.html", {"request":request,"stocks":rows})

@app.get("/stock/{symbol}")
def stock_view(request:Request, symbol):
    handler.connect()
    prices = handler.getPricesBySymbol(symbol)
    return templates.TemplateResponse("stock_view.html", {"request":request, "symbol":symbol, "prices":prices})