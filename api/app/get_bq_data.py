
from google.cloud import bigquery 
from google.oauth2 import service_account

def get_bq_data():
    # Chemin vers votre fichier de clé JSON
    key_path = r'/Users/paulvallee/Desktop/MAS/M2/Tech IA/Projet/Groupe_4/credentials/sa-key-group-4.json'
    
    # Créez les credentials
    credentials = service_account.Credentials.from_service_account_file(key_path)
    
    # Créez le client BigQuery
    client = bigquery.Client(credentials=credentials)
    
    return client


