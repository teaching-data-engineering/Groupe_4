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

# Initialisation de l'application FastAPI
app = FastAPI()

# Connexion à BigQuery
client = get_bq_data()

# Spécification de la table dans BigQuery
data = "`dataset_groupe_4.enrich`"


# Inclusion des routers
app.include_router(gets_endpoints.router)
app.include_router(puts_endpoints.router)
