# Import des modules nécessaires pour l'application FastAPI et la gestion des données
from typing import Optional
from datetime import date
from fastapi import APIRouter
from fastapi import HTTPException
from pagination import display_data
from get_bq_data import get_bq_data  # Importation d'une fonction pour récupérer les données de BigQuery
from difflib import SequenceMatcher  # Pour la recherche approximative de correspondance de noms
import pandas as pd
from joblib import load  # Pour charger des modèles enregistrés (ex: Random Forest)
# Initialisation de l'application FastAPI
router = APIRouter()

# Connexion à BigQuery
client = get_bq_data()

# Spécification de la table dans BigQuery
data = "`dataset_groupe_4.enrich`"


@router.put("/events/update-events")
async def update_events_informations(
    remplacement_type: str,  # Type à remplacer, doit être un des champs de la base
    new_value: str,  # Nouvelle valeur pour le champ
    lieu: Optional[str] = None,  # Nom du lieu à filtrer
    artist: Optional[str] = None,  # Nom de l'artiste à filtrer
    date: Optional[str] = None  # Date à filtrer
):
    # Liste des champs autorisés pour la mise à jour
    valid_fields = ["startsAt", "artistName", "venueName"]

    # Validation du champ de remplacement
    if remplacement_type not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid replacement type '{remplacement_type}'. Must be one of {valid_fields}."
        )

    # Construction des conditions pour la clause WHERE
    conditions = []
    if lieu:
        conditions.append(f"venueName = '{lieu}'")
    if artist:
        conditions.append(f"artistName = '{artist}'")
    if date:
        conditions.append(f"startsAt = '{date}'")

    # Si aucune condition n'est fournie, lever une erreur
    if not conditions:
        raise HTTPException(
            status_code=400,
            detail="At least one condition (lieu, artist_new, or date) must be provided."
        )

    # Construction de la clause WHERE
    where_clause = " AND ".join(conditions)

    # Construction de la requête SQL
    query = f"""
        UPDATE {data} 
        SET {remplacement_type} = '{new_value}'
        WHERE {where_clause}
    """

    # Exécution de la requête SQL
    query_job = client.query(query)
    query_job.result()  # Attente de l'exécution complète

    return {"message": f"The field '{remplacement_type}' has been updated successfully for the specified conditions {conditions}."}





    