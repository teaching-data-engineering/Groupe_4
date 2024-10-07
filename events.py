import requests
import time

# date : today, all-dates, this-month ,this-week, 
def get_events(page=2, start_date="2024-10-07" ,end_date = "2024-10-30" ):
    
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
        "date" : start_date + "T00%3A00%3A00%2C" + end_date + "T23%3A00%3A00"
    }

    # On spécifie l'URL de la requête puis on l'envoie
    url = "https://www.bandsintown.com/choose-dates/fetch-next/upcomingEvents"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, params=params)

    # Vérification de la réponse
    if response.status_code != 200:
        print(f"Erreur lors de la requête pour la page {page}")
        return all_events

    data = response.json()

    # On récupère les événements
    events = data.get("events")

    if not events:
        print(f"Aucun événement trouvé pour la page {page}")
        return all_events

    # On enregistre les événements
    all_events.extend(events)

    # On affiche les événements
    for event in events:
        artist = event.get("artistName")
        venue = event.get("venueName")
        date = event.get("startsAt")
        print(artist, venue, date)

    return all_events


if '__main__' == __name__:
    data = get_events(page=1)
    print(data)
import requests
import time