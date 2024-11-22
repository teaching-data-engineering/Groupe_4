from typing import Annotated
from fastapi import Depends, FastAPI, Header, HTTPException
import json

app = FastAPI()

# Lire le fichier JSON contenant le token utilisateur
with open('token_user.json') as f:
    token_data = json.load(f)

# La fonction de vérification du token utilisateur
async def verify_token_user(x_token: Annotated[str, Header()]):
    if x_token != token_data["token-user"]:  # Comparaison avec le token "token-user"
        raise HTTPException(status_code=403, detail="X-Token header invalid")

# Endpoint avec dépendance sur verify_token
@app.get("/items/", dependencies=[Depends(verify_token_user)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]
