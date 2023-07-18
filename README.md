# webapp-stock-project

Background
--------
We wanted to create a dashboard where the user could compare two stock tickers through different metrics, plots, and charts. This dashboard allows you to browse and relate helpful financial information about the top 100 US companies from [Yahoo finance](https://finance.yahoo.com/).

## Objectives ##

### Webscapers and Database
The data for this project were pulled from Yahoo Finance, as mentioned above, with the yfinance module in Python running locally. Additional data were pulled from https://companiesmarketcap.com/usa/largest-companies-in-the-usa-by-market-cap/ in order to get the list of companies that we were working with. All of these data were loaded into a MySQL database on AWS. We used AWS Lambda services, written in Python, and triggered with a AWS APIGateway API, to make these data available via an open API. The database itself, while hosted on AWS, is managed locally with MySQLWorkbench.
The folder "stock_scrape_load" contains the code and the data associated with the daily data pulls. The subfolder "jobs" contains the python code, the subfolder "data" contains the daily output data as well as the SQL dumps files that were used to upload this to the RDS MySQL database. There was an attempt to write another script to load the data automatically but it was not debugged in time. We also saved the historical company stock data in csv and JSON formats for easy local development.
The Lambda code is in the main folder. The files are:
* company_addresses_lambda.py
* top_100_tickers_query_lambda.py
* stock_data_lambda.py -- this one works but the API Gateway API is having CORS issues that we could not fully resolve. A screenshot shows it working from local machine.

### Flask App Deployment

### Visualization Dashboard
This dahsboard has two dropdown menus, from which the user selects two different stocks to comapre. The comparisions include:
- #### Information about each stock:
  - the ticker
  - date of information
  - sector
  - 52 week change
  - ask
  - bid
  - 52 week high/low
  - daily open
  - previous close
  - daily volume
  - quick ratio
  - 10 day average volume
  - marketcap
- #### OHLC (open high low close) chart

- #### Gauge Chart comparing:
  - previous close
  - 52 week high/low
  - delta being the difference between previous close and 52 week low

<img width="782" alt="Screenshot 2023-07-17 at 8 55 23 PM" src="https://github.com/gmitt98/webapp-stock-project/assets/127706155/33aa8a6f-d03e-4458-b308-fe91287f8aba">

### Interactive Map
