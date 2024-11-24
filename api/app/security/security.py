from typing import Annotated
from fastapi import Header, HTTPException
import json

# Lire le fichier JSON contenant le token utilisateur
with open('api/app/security/token_user.json') as f:
    token_data = json.load(f)

# La fonction de vérification du token utilisateur
async def verify_token_user(x_token: Annotated[str, Header()]):
    if x_token != token_data["token-user"]:  # Comparaison avec le token "token-user"
        raise HTTPException(status_code=403, detail="X-Token header invalid")
