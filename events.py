import requests
import re
import time
import pickle
import datetime
import os.path

def fetch_page(link):
    time.sleep(0.5)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(link,headers=headers)
    if r.status_code == 403:
        print("err 403 : "+link)
        return {}
    else:
        return r.json()

def fetch_date(date):
    delta = datetime.timedelta(hours = 24)
    link_before = "https://www.bandsintown.com/choose-dates/fetch-next/upcomingEvents?city_id=2950159&date="
    date_str = f"{date.strftime('%Y-%m-%d')}T00%3A00%3A00%2C{(date+delta).strftime('%Y-%m-%d')}T23%3A00%3A00"
    link_after = "&page=1&longitude=13.41053&latitude=52.52437&genre_query=all-genres"
    concerts = []
    link = link_before + date_str + link_after
    while link != None:
        dico = fetch_page(link)
        link = dico.get("urlForNextPageOfEvents",None)
        concerts += dico.get("events",[])
    return concerts


def fetch_month():
    now = datetime.datetime.now()
    delta = datetime.timedelta(hours = 24)
    date = now
    for i in range(1,32):
        path = f'data/concerts{(date+delta).strftime("%y-%m-%d")}.pkl'
        if(not os.path.isfile(path)):
            concerts = fetch_date(date)
            save(concerts,path)
        date = date + delta

def save(concerts,path):
    with open(path, 'wb') as f:
       pickle.dump(concerts, f)

def main():
    fetch_month()

if __name__=="__main__": 
    main()
