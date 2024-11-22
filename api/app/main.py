# !pip install fastapi uvicorn 
# !pip install db_dtypes

from typing import Union
from fastapi import FastAPI
import get_bq_data 
import pandas as pd
from fastapi.responses import HTMLResponse
import datetime

app = FastAPI()
client = get_bq_data.get_client()


def display_data(data, end_point, page = 1):
    url = f"127.0.0.1:8000/"
    total_results = len(data)
    results_per_page = 10
    total_pages = total_results // results_per_page
    next_page_url = url + f"{end_point}?page={page + 1}" if page < total_pages else None
    data_display = data[(page - 1) * results_per_page: page * results_per_page]
    display = {"metadata":{"page": page,"total_pages": total_pages ,"total_results": total_results, "next_page_url": next_page_url}}
    return {"data":data_display}, display


from pydantic import BaseModel
class Objet(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

# endpoin root
@app.get("/", response_class=HTMLResponse)
async def root():
    # HTML stylé pour la page d'accueil
    message = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bienvenue sur notre API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin: 2em;
                background-color: #f4f4f9;
                color: #333;
            }
            h1 {
                color: #4CAF50;
            }
            a {
                color: #4CAF50;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            .container {
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <h1>Bienvenue sur notre API</h1>
        <p>Ci-dessous vous trouverez les fonctionnalités disponibles :</p>
        <div class="container">
            <p><a href="/docs" target="_blank">📄 Documentation de l'API</a></p>
            <p><a href="/events" target="_blank">📅 Liste des événements</a></p>
            <p><a href="/events/by-day-of-week" target="_blank">📊 Événements par jour de la semaine</a></p>
        </div>
    </body>
    </html>
    """
    return message


@app.get("/events")
async def get_events(page: int = 1):
    query = f"""select * 
    from `dataset_groupe_4.enrich`
    """
    
    # Exécutez la requête
    query_job = client.query(query)
    
    # Récupérez les résultats
    results = query_job.result()
    
    # Récupérer les données en liste de dictionnaires
    data = [dict(row) for row in results]
    
    display = display_data(data, "events", page)
    
    return display


@app.get("/events/by-day-of-week")
async def get_events_by_day_of_week(page: int = 1, week: str = None):
    query = f"""select * 
    from `dataset_groupe_4.enrich`
    """
    
    # Exécutez la requête
    query_job = client.query(query)
    
    # Récupérez les résultats
    df = query_job.result().to_dataframe()
    df['startsAt'] = pd.to_datetime(df['startsAt'])
    df['day_of_week'] = df['startsAt'].dt.day_name()
    df['week'] = df['startsAt'].dt.isocalendar().week
    if week:
        df = df.query(f"week == {week}")
    df_day_of_week = df.groupby('day_of_week')["day_of_week"].count()
    
    # convert to dictionary
    data = df_day_of_week.to_dict()
     
    return data

@app.put("/events/update-artist")
async def update_artist(artist_old: str, lieu: str, artist_new: str):
    query = f"""update `dataset_groupe_4.enrich` 
    set artistName = '{artist_new}'
    where artistName = '{artist_old}' and venueName = '{lieu}'
    """
    
    # Exécutez la requête
    query_job = client.query(query)
    query_job.result()
    
    return {"message": "Artist Name updated successfully"}

@app.put("/events/update-venue")
async def update_venue(venue_old: str, venue_new: str, artist: str):
    query = f"""update `dataset_groupe_4.enrich` 
    set venueName = '{venue_new}'
    where venueName = '{venue_old}'and artistName = '{artist}'
    """
    
    # Exécutez la requête
    query_job = client.query(query)
    query_job.result()
    
    return {"message": "Venue Name updated successfully"}
    
    