import yfinance as yf
import json
import csv

ticker = 'GOOG'

my_stock = yf.Ticker(ticker)

print(my_stock.info)
