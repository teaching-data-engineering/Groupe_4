from api.app.get_bq_data import get_bq_data

data = "`dataset_groupe_4.enrich`"
client = get_bq_data()

query = f"""select * 
from  {data}
"""



# Exécutez la requête
query_job = client.query(query)

# Récupérez les résultats
results = query_job.result()

# Récupérer les données en liste de dictionnaires
result_data = [dict(row) for row in results]
print(result_data)