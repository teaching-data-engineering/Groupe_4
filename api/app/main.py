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



    
    