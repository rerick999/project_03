from bs4 import BeautifulSoup
import requests
import csv
import yfinance as yf
import geopy
import time
import json
MAX=None

class MC_Scraper:
    def __init__(self,target_url):
        print('initializing...')
        self.target_url=target_url
        self.locator=geopy.Nominatim(user_agent='myGeocoder')
        self.dd={}

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
                if not company_ticker in self.dd:
                    self.dd[company_ticker]={'ticker':company_ticker,'name':company_name}
            except:
                pass

    def get_additional_data(self):
        print('getting additional data...')
        for i,co in enumerate(self.dd):
            if MAX and i>MAX: break
            print('.',end='')
            time.sleep(1)
            ticker=co
            tickerobj=yf.Ticker(ticker)
            info=tickerobj.info
##            print(info)
            #get quick ratio
            try:
                self.dd[co]['quick_ratio']=info['quickRatio']
            except:
                self.dd[co]['quick_ratio']=0.00
            #get market cap
            try:
                self.dd[co]['market_cap']=info['marketCap']
            except:
                print('no market cap for: %s'%co)
##                self.dd[co]['market_cap']=0.00
            #get address
            try:
                fields=['address1','city','state','zip','country']
                address=[info[x] for x in fields]
            except:
                try:
                    fields=['city','state','zip','country']
                    address=[info[x] for x in fields]
                except:
                    print('\n-'*10+'>no address found for %s'%ticker)
            self.dd[co]['address']=address
            #get lat and lon
            latlon=self.get_latlon(address)
            if latlon:
                self.dd[co]['lat'],self.dd[co]['lon']=latlon
            else:
                print('\n-'*10+'>'+'no latlon found for %s'%co)
            #fix address
            self.dd[co]['address']=', '.join(self.dd[co]['address'])

    def get_latlon(self,address):
        latlon=self.get_latlon2(address)
        i=0
        while latlon==[] and i<len(address):
            latlon=self.get_latlon2(address[i:])
            if latlon:
                break
            else:
                i+=1
        return latlon

    def get_latlon2(self,address):
        address_str=', '.join(address)
        try:
            location=self.locator.geocode(address_str)
            latlon=[location.latitude,location.longitude]
        except:
            return []
        return latlon

    def print_dd(self):
        for d in sorted(self.dd):
            print(d,self.dd[d])

    def save_to_json(self,fpth):
        print('\nsaving to file: %s...'%fpth)
        with open(fpth, 'w', newline='\n') as fobj:
            fobj.write('[')
            for i,co in enumerate(sorted(self.dd)):
                if i==0:
                    fobj.write('\n')
                else:
                    fobj.write('\n,')
                json.dump(self.dd[co],fobj)
            fobj.write('\n]')


if __name__=='__main__':
    url = "https://companiesmarketcap.com/usa/largest-companies-in-the-usa-by-market-cap"
    mc=MC_Scraper(url)
    mc.get_data()
    mc.get_additional_data()
##    mc.print_dd()
##    mc.save_to_csv('top_100_company_tickers.csv')
    mc.save_to_json('../leaflet/data.geojson')
    
