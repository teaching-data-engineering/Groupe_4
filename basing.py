import pandas_gbq
from google.oauth2 import service_account 

def data_to_gbq(df, replace=False):
    credentials = service_account.Credentials.from_service_account_file('credentials/sa-key-group-4.json')
    table_id = "dataset_groupe_4.enrich"
    project_id = "ai-technologies-ur2"
    
    if replace:
        pandas_gbq.to_gbq(df, table_id, project_id=project_id, credentials=credentials, if_exists='replace')
    else:
        try:
            pandas_gbq.to_gbq(df, table_id, project_id=project_id, credentials=credentials, if_exists='append')
        except pandas_gbq.gbq.TableCreationError as e:
            print(f"Erreur de création de table : {e}")
            print("La table existe déjà. Les données seront ajoutées à la table existante.")
            pandas_gbq.to_gbq(df, table_id, project_id=project_id, credentials=credentials, if_exists='append')