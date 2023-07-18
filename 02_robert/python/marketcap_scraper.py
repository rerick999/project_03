# this code does a one-time scrape of companiesmarketcap website and saves the data in a csv

from bs4 import BeautifulSoup
import requests
import csv
import yfinance as yf
import geopy
import time

class MC_Scraper:
    def __init__(self,target_url):
        print('initializing...')
        self.target_url=target_url
        self.locator=geopy.Nominatim(user_agent='myGeocoder')
        self.datalist=[]

    def get_data(self):
        print('getting data...')
        response=requests.get(self.target_url)
        soup=BeautifulSoup(response.content, "html.parser")
        tds=soup.find_all("td")
        for td in tds:
            try:
                company_name=td.find("div", class_="company-name").text
                company_name=company_name.strip()
                company_ticker=td.find("div", class_="company-code").text
                company_ticker=company_ticker.strip()
##                print(company_name,company_ticker)
                self.datalist+=[[company_name,company_ticker]]
            except:
                pass

    def get_additional_data(self):
        print('getting additional data...')
        for i,d in enumerate(self.datalist):
            print('.',end='')
            time.sleep(1)
            ticker=d[1]
            tickerobj=yf.Ticker(ticker)
            info=tickerobj.info
            #
            data=[]
            #
            try:
                data+=[[info['quickRatio']]]
            except:
                data+=[[0.0]]
            #
            try:
                fields=['address1','city','state','zip','country']
                address=[info[x] for x in fields]
            except:
                try:
                    fields=['city','state','zip','country']
                    address=[info[x] for x in fields]
                except:
                    print('-'*10+'>no address found for %s'%ticker)
            data+=[address]
            #
            latlon=self.get_latlon(address)
            print(address,latlon)
            #
            data+=[latlon]
            d+=data
##            print(data)

    def get_latlon(self,address):
        latlon=self.get_latlon2(address)
        if latlon==[]:
            latlon=self.get_latlon2(address[1:])
        return latlon

    def get_latlon2(self,address):
        address_str=', '.join(address)
        try:
            location=self.locator.geocode(address_str)
            latlon=[location.latitude,location.longitude]
        except:
            return []
        return latlon
        

    def print_list(self):
        for l in self.datalist:
            print(l)

    def save(self,fpth):
        print('saving to file: %s...'%fpth)
        with open(fpth, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Name', 'Ticker'])
            writer.writerows(self.datalist)


if __name__=='__main__':
    url = "https://companiesmarketcap.com/usa/largest-companies-in-the-usa-by-market-cap"
    mc=MC_Scraper(url)
    mc.get_data()
    mc.get_additional_data()
    mc.print_list()
##    mc.save('top_100_company_tickers.csv')
    
