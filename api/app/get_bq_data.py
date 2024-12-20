#! pip install google-cloud-bigquery
#! pip install google-auth
from google.cloud import bigquery 
from google.oauth2 import service_account

# Fonction pour récupérer le client BigQuery
def get_client():
    # Chemin vers votre fichier de clé JSON
    key_path = r'credentials/sa-key-group-4.json'
    
    # Créez les credentials
    credentials = service_account.Credentials.from_service_account_file(key_path)
    
    # Créez le client BigQuery
    client = bigquery.Client(credentials=credentials)
    
    return client
