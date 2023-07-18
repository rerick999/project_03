import os
current_directory = os.getcwd()
file_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_directory)

import yfinance as yf
import json
import csv
from datetime import date
today_date = date.today()

data = []  

with open('../top_100_company_tickers.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        ticker = row['Ticker']
        print("Processing", ticker)
        my_stock = yf.Ticker(ticker)

        my_info = {
            "ticker": ticker,
            "date": str(today_date),
            "sector": None,
            "52WeekChange": None,
            "ask": None,
            "bid": None,
            "52WeekHigh": None,
            "52WeekLow": None,
            "dailyOpen": None,
            "previousClose": None,
            "dailyVolume": None,
            "quickRatio": None,
            "10DayAverageVolume": None,
            "marketCap": None,
            "dayHigh" : None,
            "dayLow" : None,
        }

        try:
            my_info["sector"] = my_stock.info["sector"]
            my_info["52WeekChange"] = my_stock.info["52WeekChange"]
            my_info["ask"] = my_stock.info["ask"]
            my_info["bid"] = my_stock.info["bid"]
            my_info["52WeekHigh"] = my_stock.info["fiftyTwoWeekHigh"]
            my_info["52WeekLow"] = my_stock.info["fiftyTwoWeekLow"]
            my_info["dailyOpen"] = my_stock.info["open"]
            my_info["previousClose"] = my_stock.info["previousClose"]
            my_info["dailyVolume"] = my_stock.info["volume"]
            my_info["quickRatio"] = my_stock.info["quickRatio"]
            my_info["10DayAverageVolume"] = my_stock.info["averageDailyVolume10Day"]
            my_info["marketCap"] = my_stock.info["marketCap"]
            my_info["dayHigh"] = my_stock.info["dayHigh"]
            my_info["dayLow"] = my_stock.info["dayLow"]
        except KeyError as e:
            print("Key not found for ticker:", ticker)
            print("Error:", e)

        data.append(my_info)

json_filename = os.path.join("..", f"data/stock_data_{today_date}.json")
with open(json_filename, 'w') as json_file:
    json.dump(data, json_file, indent=4)

csv_filename = os.path.join("..",f"data/stock_data_{today_date}.csv")
with open(csv_filename, 'w', newline='') as csv_file:
    fieldnames = data[0].keys() if data else [] 
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
    
print("Data saved")
