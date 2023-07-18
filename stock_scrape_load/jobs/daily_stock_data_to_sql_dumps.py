import csv
from datetime import date
import os
current_directory = os.getcwd()
file_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_directory)

today_date = date.today()
csv_filename = os.path.join("..",f"data/stock_data_{today_date}.csv")
sql_dump_filename = os.path.join("..", f"data/stock_data_{today_date}.sql")

with open(csv_filename, "r") as csv_file, open(sql_dump_filename, "w") as sql_dump_file:
    csv_reader = csv.reader(csv_file)
    header = next(csv_reader)

    for row in csv_reader:
        ticker, date, sector, week_change, ask, bid, high, low, daily_open, prev_close, volume, ratio, avg_volume, market_cap, dayHigh, dayLow = row
        row_values = [ticker, date, sector, week_change, ask, bid, high, low, daily_open, prev_close, volume, ratio, avg_volume, market_cap, dayHigh, dayLow]
        row_values = ["NULL" if value == "" else value for value in row_values]

        sql_insert = "INSERT INTO myfinancedb.stock_data (ticker, date, sector, 52WeekChange, ask, bid, 52WeekHigh, 52WeekLow, dailyOpen, previousClose, dailyVolume, quickRatio, 10DayAverageVolume, marketCap, dayHigh, dayLow) VALUES "
        sql_values = f"('{row_values[0]}', '{row_values[1]}', '{row_values[2]}', {row_values[3]}, {row_values[4]}, {row_values[5]}, {row_values[6]}, {row_values[7]}, {row_values[8]}, {row_values[9]}, {row_values[10]}, {row_values[11]}, {row_values[12]}, {row_values[13]}, {row_values[14]}, {row_values[15]});\n"

        sql_dump_file.write(sql_insert + sql_values)

print("SQL dump file created successfully.")
