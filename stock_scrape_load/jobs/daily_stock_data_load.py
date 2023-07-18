import os
current_directory = os.getcwd()
file_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_directory)

import csv
import mysql.connector
from datetime import date

today_date = date.today()

import config

print(config.myhost)

sql_dump_file = os.path.join("..", f"data/stock_data_{today_date}.sql")
with open(sql_dump_file, "r") as file:
    sql_dump_text = file.read()
    print(sql_dump_text)

#csv_filename = f"stock_data_{today_date}.csv"

try:
    connection = mysql.connector.connect(
        host=config.myhost,
        database=config.mydatabase,
        user=config.myuser,
        password=config.mypassword
        )
    
    cursor = connection.cursor()
    cursor.execute(sql_dump_text, multi=True)

    results = cursor.fetchall()
    print(results)
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()