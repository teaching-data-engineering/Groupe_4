# Import des modules nécessaires pour l'application FastAPI et la gestion des données
from typing import Optional
from datetime import date
from fastapi import FastAPI
from fastapi import HTTPException
from get_bq_data import get_bq_data  # Importation d'une fonction pour récupérer les données de BigQuery
from pagination import display_data
from difflib import SequenceMatcher  # Pour la recherche approximative de correspondance de noms
import pandas as pd
from endpoints import gets_endpoints, puts_endpoints
from joblib import load  # Pour charger des modèles enregistrés (ex: Random Forest)
from fastapi.responses import HTMLResponse

# Initialisation de l'application FastAPI
app = FastAPI()

# Connexion à BigQuery
client = get_client()

# Spécification de la table dans BigQuery
data = "`dataset_groupe_4.enrich`"

# endpoint de la page d'accueil

@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Accueil API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f4f4f4;
            }
            h1 {
                color: #333;
            }
            ul {
                list-style-type: none;
                padding: 0;
            }
            li {
                margin: 10px 0;
            }
            a {
                text-decoration: none;
                color: #007BFF;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>🎉 Bienvenue sur HotPerf, l'Api évènementielle 🎉</h1>
        <p>Ci-dessous, vous trouverez les fonctionnalités disponibles :</p>
        <ul>
            <li><a href="/docs">📄Documentation de l'API</a></li> 
            <li><a href="/events">📅Liste des événements</a></li>
            <li><a href="/events/by-day-of-week">📊Événements par jour de la semaine</a></li>
            <li><a href="/events/search">🔍Rechercher des événements</a></li>
            <li><a href="/events/artist">🎤Rechercher par artiste</a></li>
            <li><a href="/events/by-venue">📍Statistiques des événements par lieu</a></li>
            <li><a href="/events/streaming-vs-in-person">🖥️Comparaison streaming vs en personne</a></li>
            <li><a href="/events/is_popular">⭐Prédire la popularité des événements</a></li>
        </ul>
        <p>🚀 En cas de difficulté vous pouvez consulter la <a href="/docs">documentation de l'API</a> pour plus d'informations.</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)



# Inclusion des routers
app.include_router(gets_endpoints.router)
app.include_router(puts_endpoints.router)
