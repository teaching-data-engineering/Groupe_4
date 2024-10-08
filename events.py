import requests
import re
import time
import pickle
import pandas as pd 

def fetch_page(link):
    time.sleep(0.5)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(link,headers=headers)
    if r.status_code == 403:
        return {}
    else:
        return r.json()

def fetch_date(date):
    link_before = "https://www.bandsintown.com/choose-dates/fetch-next/upcomingEvents?city_id=2950159&date="
    date = f"2024-10-{date:02d}T00%3A00%3A00%2C2024-10-{date+1:02d}T23%3A00%3A00"
    link_after = "&page=1&longitude=13.41053&latitude=52.52437&genre_query=all-genres"
    concerts = []
    link = link_before + date + link_after
    while link != None:
        dico = fetch_page(link)
        link = dico.get("urlForNextPageOfEvents",None)
        concerts += dico.get("events",[])
    return concerts


def fetch_month():
    dates = range(1,32)
    results = map(fetch_date,dates)
    return [concert for concerts in results for concert in concerts]

def save(concerts):
    with open('concerts.pkl', 'wb') as f:
       pickle.dump(concerts, f)




def main():
    concerts = fetch_month()
    save(concerts)

if __name__=="__main__": 
    main()
    