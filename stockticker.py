from __future__ import division
from flask import Flask, render_template, request
import requests
import pandas as pd
import pandas_datareader.data as web
import urllib3
import re
import requests
from time import sleep
from urllib.request import urlopen
import datetime
import sys
from bs4 import BeautifulSoup
from googlefinance import getQuotes
import json

def getprice(symbol):
    quote=web.get_quote_yahoo(symbol)
    price_char = str(quote['last'])
    price_64 =  re.sub("[^.0-9]", "", price_char)
    price_untrim = price_64[:-2]
    price_quotes=price_untrim.replace(" ","")
    price=price_quotes.replace("'","")
    return price

app = Flask(__name__)

@app.route('/stocks', methods=['POST'])
def stocks():
    zip = request.form['ticker']
    r = requests.get("http://d.yimg.com/autoc.finance.yahoo.com/autoc?region=All&lang=en-us&query="+zip)
    json_object = r.json()
    name_company = json_object['ResultSet']['Result'][0]['name']
    company_ticker = json_object['ResultSet']['Result'][0]['symbol']
    quote=getQuotes(company_ticker)[0]['LastTradePrice']
    return render_template('temperature.html', temp=name_company, symbol=company_ticker, price=quote)
	

@app.route('/')
def index():
	return render_template('index1.html')

if __name__ == '__main__':
    app.run(debug=True)