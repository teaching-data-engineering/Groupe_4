#! pip install google-cloud-bigquery
#! pip install google-auth
from google.cloud import bigquery 
from google.oauth2 import service_account
import pandas as pd

def get_bq_data():
    # Chemin vers votre fichier de clé JSON
    key_path = r'credentials/sa-key-group-4.json'
    
    # Créez les credentials
    credentials = service_account.Credentials.from_service_account_file(key_path)
    
    # Créez le client BigQuery
    client = bigquery.Client(credentials=credentials)
    
    # Exécutez la requête
    query = f"""select * 
    from `ai-technologies-ur2.dataset_groupe_4.enrich`
    """
    
    # Exécutez la requête
    query_job = client.query(query)
    
    # Récupérez les résultats
    results = query_job.result()
    data = results.to_dataframe()
    
    return data

def get_client():
    # Chemin vers votre fichier de clé JSON
    key_path = r'credentials/sa-key-group-4.json'
    
    # Créez les credentials
    credentials = service_account.Credentials.from_service_account_file(key_path)
    
    # Créez le client BigQuery
    client = bigquery.Client(credentials=credentials)
    
    return client
