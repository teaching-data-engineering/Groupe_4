# !pip install fastapi uvicorn 
# !pip install db_dtypes

from typing import Union
from fastapi import FastAPI
import get_bq_data 
import pandas as pd
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
