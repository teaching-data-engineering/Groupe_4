import requests
import json

# URL de l'API
url = "http://127.0.0.1:8000/items/"

# Charger le token depuis le fichier JSON
with open('token_user.json') as f:
    token_data = json.load(f)

# Ajouter le token "token-user" dans les headers
headers = {
    "X-Token": token_data["token-user"]
}

# Effectuer une requête GET
response = requests.get(url, headers=headers)

# Afficher le résultat
if response.status_code == 200:
    print("Requête réussie :", response.json())
else:
    print(f"Erreur {response.status_code} :", response.json())
