from typing import Union
from fastapi import FastAPI, HTTPException
from ..get_bq_data import get_bq_data

app = FastAPI()

data_str = "ai-technologies-ur2.dataset_groupe_4.enrich"

@app.get("/events/{by-day-of-week}")
async def read_item(by_day_of_week: Union[int, None] = None):
    query = f"""
                SELECT * 
                FROM {data_str} 
                WHERE WEEK(day_of_week) = '{by_day_of_week}'
            """

    try:
        result = get_bq_data().query(query)

        data = [dict(row) for row in result]
        return data
    
    except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


