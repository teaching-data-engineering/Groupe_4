

from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd

# Chemin vers votre fichier de clé JSON
key_path = 'C:\kevin\M2\\technologie_IA\TD 1\Group 4\sa-key-group-4.json'

# Créez les credentials
credentials = service_account.Credentials.from_service_account_file(
    key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

# Créez le client BigQuery
client = bigquery.Client(credentials=credentials, project=credentials.project_id)