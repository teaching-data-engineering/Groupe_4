import pandas_gbq
from google.oauth2 import service_account 

def data_to_gbq(df):
    credentials = service_account.Credentials.from_service_account_file( 'sa-key-group-4.json', )
    pandas_gbq.to_gbq(df,"dataset_groupe_4.non_enrich", project_id="ai-technologies-ur2",credentials = credentials ) 