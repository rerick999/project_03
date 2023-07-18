import subprocess
from datetime import date
today_date = date.today()

import os
current_directory = os.getcwd()
file_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_directory)

scrape = "jobs/daily_stock_data_scrape.py"
load = "jobs/daily_stock_data_load.py"
dump = "jobs/daily_stock_data_to_sql_dumps.py"

subprocess.run(["python", scrape])
subprocess.run(["python", dump])
#subprocess.run(["python", load])

print(f"All data scraped and saved for {today_date}.")