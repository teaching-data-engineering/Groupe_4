from google.cloud import bigquery 
from google.oauth2 import service_account


def get_bq_data():
    credentialsPath = r'credientials/sa-key-group-4.json'

    credentials = service_account.Credentials.from_service_account_file(credentialsPath)

    client = bigquery.Client(credentials=credentials)

    return client





