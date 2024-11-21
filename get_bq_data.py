#! pip install google-cloud-bigquery
#! pip install google-auth
from google.cloud import bigquery 
from google.oauth2 import service_account
from pprint import pprint

def get_bq_data(limit=5):
    # Chemin vers votre fichier de clé JSON
    key_path = r'credentials/sa-key-group-4.json'
    
    # Créez les credentials
    credentials = service_account.Credentials.from_service_account_file(key_path)
    
    # Créez le client BigQuery
    client = bigquery.Client(credentials=credentials)
    
    # Exécutez la requête
    query = f"""select * 
    from `dataset_groupe_4.enrich`
    limit {limit};
    """
    
    # Exécutez la requête
    query_job = client.query(query)
    
    # Récupérez les résultats
    results = query_job.result()
    
    # Récupérer les données en liste de dictionnaires
    data = [dict(row) for row in results]
    
    return data

credentialsPath = r'credentials/sa-key-group-4.json'
credentials = service_account.Credentials.from_service_account_file(credentialsPath)

client = bigquery.Client(credentials=credentials)

query = """select * 
from `dataset_groupe_4.enrich`
limit 5;
"""

result = client.query(query)

# Afficher les résultats
pprint([dict(row) for row in result])