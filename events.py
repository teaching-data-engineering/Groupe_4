import requests
import time
import re 


# date : today, all-dates, this-month, this-week
def get_json(start_date, end_date, page=1):
    all_events = []

    # Initialisation des paramètres de la requête
    params = {
        "came_from": "257",
        "utm_medium": "web",
        "utm_source": "home",
        "utm_campaign": "top_event",
        "sort_by_filter": "Number+of+RSVPs",
        "concerts": "true",
        "page": page,
        "longitude": "13.41053",
        "latitude": "52.52437",
        "genre_query": "all-genres",
        "date": f"{start_date}T00%3A00%3A00%2C{end_date}T23%3A00%3A00"
    }

    # On spécifie l'URL de la requête puis on l'envoie
    url = "https://www.bandsintown.com/choose-date/fetch-next/upcomingEvents"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, params=params)

    # Vérification de la réponse
    if response.status_code != 200:
        print(f"Erreur lors de la requête pour la page {page}: {response.status_code}")
        print(f"Response Text: {response.text}")
        return all_events

    data = response.json()

    return data 



def check_next_page(data):
    next_url = data.get("urlForNextPageOfEvents")
    if next_url is not None:
        return re.search(r"page=\d+",next_url ).group(0).split("=")[1]
    else :
        return None


def get_all_events(start_date, end_date):
   
    all_events = []

    #Creer un vecteur contenant toute les dates entre start_date et end_date
    all_dates = [time.strftime("%Y-%m-%d", time.strptime(str(i), "%j")) for i in range(time.strptime(start_date, "%Y-%m-%d").tm_yday, time.strptime(end_date, "%Y-%m-%d").tm_yday + 1)]
    page = 1 
    for date in range(len(all_dates)-1):
        data = get_json(page=page, start_date=all_dates[date], end_date=all_dates[date+1])
        while data:
            all_events.extend(data.get("events"))
            next_page = check_next_page(data)
            if next_page is not None:
                page = get_json(page=next_page,start_date=all_dates[date], end_date=all_dates[date+1])
            else:
                break
    return all_events







if '__main__' == __name__:
    data = get_all_events(start_date = "2024-10-08", end_date = "2024-10-10")
   
