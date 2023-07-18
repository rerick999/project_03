from bs4 import BeautifulSoup
import requests
import csv
import yfinance as yf
import geopy
import time
import json
import sys
MAX=None

class MC_Scraper:
    def __init__(self,target_url):
        print('initializing...',file=sys.stderr)
        self.target_url=target_url
        self.locator=geopy.Nominatim(user_agent='myGeocoder')
        self.dd={}

    def get_data(self):
        print('getting data...',file=sys.stderr)
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
        print('getting additional data...',file=sys.stderr)
        cos=sorted(self.dd.keys())
        for i,co in enumerate(cos):
            if MAX and i>MAX: break
            print('.',end='',file=sys.stderr)
            time.sleep(1)
            ticker=co
            info=self.get_info(ticker)
            if not info: continue
            #get quick ratio
            try:
                self.dd[co]['quick_ratio']=info['quickRatio']
            except:
                self.dd[co]['quick_ratio']=0.00
            #get market cap
            try:
                self.dd[co]['market_cap']=info['marketCap']
            except:
                print('no market cap for: %s'%co,file=sys.stderr)
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
                    print('\n-'*10+'>no address found for %s'%ticker,file=sys.stderr)
            try:
                self.dd[co]['address']=address
                print('got address for %s'%co)
            except:
                continue
            #get lat and lon
            latlon=self.get_latlon(address)
            if latlon:
                self.dd[co]['lat'],self.dd[co]['lon']=latlon
            else:
                print('\n-'*10+'>'+'no latlon found for %s'%co,file=sys.stderr)
            #fix address
            self.dd[co]['address']=', '.join(self.dd[co]['address'])
            #get color
            self.dd[co]['color']=self.get_color(self.dd[co]['quick_ratio'])

    def get_info(self,ticker):
        try:
            tickerobj=yf.Ticker(ticker)
            info=tickerobj.info
        except:
            print('\nThere is a problem retrieving information for ticker {ticker}.\nTherefore, ticker {ticker} is being deleted.'.format(ticker=ticker),file=sys.stderr)
            del self.dd[ticker]
            return None
        return info

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

    # function color_info(depth){
    # depth=(depth*50);
    # if(depth<10)
    #     return ["red","<10"];
    # else if(depth<30)
    #     return ["orangered","10-30"];
    # else if(depth<50)
    #     return ["orange","30-50"];
    # else if(depth<70)
    #     return ["gold","50-70"];
    # else if(depth<90)
    #     return ["yellow","70-90"];
    # else {
    #     return ["green",">90"];
    #     }
    # }

    def get_color(self,qr):
        qr=qr*50
        if qr<10:
            return 'red'
        elif qr<30:
            return 'orangered'
        elif qr<50:
            return 'orange'
        elif qr<70:
            return 'gold'
        elif qr<90:
            return 'yellow'
        else:
            return 'green'

    def save_to_json(self,fpth):
        print('\nsaving to file: %s...'%fpth)
        with open(fpth, 'w', newline='\n') as fobj:
            fobj.write('let searchResults=[')
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
##    mc.save_to_json('../leaflet/data.geojson')
    mc.save_to_json('data.geojson')
    
