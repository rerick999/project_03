# this code does a one-time scrape of companiesmarketcap website and saves the data in a csv

from bs4 import BeautifulSoup
import requests
import csv

url = "https://companiesmarketcap.com/usa/largest-companies-in-the-usa-by-market-cap/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
table = soup.find("table")
for row in table.find_all("tr"):
    for cell in row.find_all("td"):
        print(cell.text)

company_data = {}

for td in table.find_all("td", class_="name-td"):
    company_name = td.find("div", class_="company-name").text
    company_ticker = td.find("div", class_="company-code").text
    company_data[company_name] = company_ticker

print(company_data)

def save_my_file(dictionary, filename):
    keys = dictionary.keys()
    values = dictionary.values()
    rows = list(zip(keys, values))
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Name', 'Ticker'])
        writer.writerows(rows)
save_my_file(company_data, 'top_100_company_tickers.csv')