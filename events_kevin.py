# Description: This script is used to fetch the events from the Bandsintown API
import requests
import re
import time
import json
import random
import pprint

"""" TD Scraping"""

"""" I - Exploration du site web """

# url de la page correspondant à notre ville et avec les spécifications demandées
# url = "https://www.bandsintown.com/choose-dates/fetch-next/upcomingEvents?city_id=2950159&date=2024-10-07T00%3A00%3A00%2C2024-10-31T23%3A00%3A00&page=1&longitude=13.41053&latitude=52.52437&genre_query=all-genres"

""" II - Utilisation de l'API """

# Question 3
"""
url = "https://www.bandsintown.com/choose-dates/fetch-next/upcomingEvents?city_id=2950159&page=1&longitude=13.41053&latitude=52.52437&genre_query=all-genres&date=2024-10-07T00%3A00%3A00%2C2024-10-31T23%3A00%3A00"

response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
data = response.json()

pprint(data)

"""


# Question 4
"""" 
url2 = "https://www.bandsintown.com/choose-dates/fetch-next/upcomingEvents?city_id=2950159&longitude=13.41053&latitude=52.52437&genre_query=all-genres"
params = {
    "date": "2024-10-07T00%3A00%3A00%2C2024-10-07T23%3A00%3A00",
    "page": 5
}

response2 = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, params=params)
data2 = response2.json()

pprint(data2)
"""

# Question 5
"""
On se rend compte que lorsque la page 23 par exemple est une page sans contenu, le champ "urlForNextPageOfEvents" est null/None.
"""

""" IV- Structurer le code pour itérer sur toutes les pages souhaitées"""

# Question 8 : Rédiger la fonction qui collecte les informations des évènements d’une page

def scrappe_one_page(link):
    time.sleep(random.uniform(0.4, 1))
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(link,headers=headers)
    if r.status_code == 403:
        return {}
    else:
        return r.json()
    
# Question 9 : Rédiger la fonction qui écrit le résultat d’une page sous le formmat JSON

def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
        


# Question 10. Rédiger la fonction qui collecte plusieurs pages

def scrap_multiple_pages(day, max_pages=33):
    link_before = "https://www.bandsintown.com/choose-dates/fetch-next/upcomingEvents?city_id=2950159&date="
    date = f"2024-10-{day:02d}T00%3A00%3A00%2C2024-10-{day+1:02d}T23%3A00%3A00"
    link_after = "&page=1&longitude=13.41053&latitude=52.52437&genre_query=all-genres"
    concerts = []
    link = link_before + date + link_after
    i = 1
    while link != None and i <= max_pages:
        dico = scrappe_one_page(link)
        link = dico.get("urlForNextPageOfEvents",None)
        concerts += dico.get("events",[])
        i += 1
    return concerts

# Question 11. Rédiger la fonction principale

def events_october():
    day = range(1,32)
    results = map(scrap_multiple_pages,day,33)
    return [concert for concerts in results for concert in concerts]  # Ici on a une liste de liste de concerts, on veut une liste de concerts

# exécution de la fonction principale

def main():
    concerts = events_october()
    save_json(concerts)


if __name__=="__main__":
    main()







