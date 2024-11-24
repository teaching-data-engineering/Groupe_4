# Import des modules nécessaires pour l'application FastAPI et la gestion des données
from typing import Optional
from datetime import date
from fastapi import APIRouter
from pagination import display_data
from get_bq_data import get_client  # Importation d'une fonction pour récupérer les données de BigQuery
from difflib import SequenceMatcher  # Pour la recherche approximative de correspondance de noms
import pandas as pd
from joblib import load  # Pour charger des modèles enregistrés (ex: Random Forest)
from security import security

# Initialisation de l'APIRouter
router = APIRouter()

# Connexion à BigQuery
client = get_client()

# Spécification de la table dans BigQuery
data = "`dataset_groupe_4.enrich`"

# Route pour obtenir tout les événements 
@router.get("/events")
async def get_events(page: int = 1, token: str = None):
    # Vérification du token utilisateur
    security.verify_token_user(token)

    query = f"""select * 
    from  {data}
    """
    
    # Exécutez la requête
    query_job = client.query(query)
    
    # Récupérez les résultats
    results = query_job.result()
    
    # Récupérer les données en liste de dictionnaires
    result_data = [dict(row) for row in results]
    
    display = display_data(result_data, "events", page)
    
    return display

# Description du champs



# Route pour rechercher des événements selon des critères facultatifs : artistName, venueName, start_date, end_date
@router.get("/events/search/")
async def event_search(
    artistName: Optional[str] = None, 
    venueName: Optional[str] = None, 
    start_date: Optional[str] = None, 
    end_date: Optional[str] = None,
    page: int = 1
):
    # Liste pour stocker les conditions de la requête SQL
    conditions = []

    # Si un nom d'artiste est fourni, on ajoute une condition pour filtrer sur cet artiste (en ignorant les majuscules et les espaces)
    if artistName:
        conditions.append(f'LOWER(REPLACE(artistName, " ", "")) = "{artistName.lower().replace(" ", "")}"')
   
    # Si un nom de lieu est fourni, on ajoute une condition pour filtrer sur ce lieu
    if venueName:
        conditions.append(f'LOWER(REPLACE(venueName, " ", "")) = "{venueName.lower().replace(" ", "")}"')
    
    # Si des dates de début ou de fin sont spécifiées, on ajoute une condition de plage de dates
    if start_date or end_date:
        if not start_date:
            start_date = "2000-01-01"  # Date de début par défaut
        if not end_date:
            end_date = date.today().strftime("%Y-%m-%d")  # Date de fin par défaut (aujourd'hui)
        conditions.append(f'startsAt BETWEEN "{start_date}T00:00:00" AND "{end_date}T23:59:59"')

    # Création de la clause WHERE en fonction des conditions
    where_clause = " AND ".join(conditions) if conditions else "1=1"  # Si aucune condition, on retourne tout

    # Construction de la requête SQL avec la clause WHERE
    query = f"""
    SELECT * FROM {data}
    WHERE {where_clause}
    """
    
    # Exécution de la requête SQL sur BigQuery
    query_job = client.query(query)
    result_data = [dict(row) for row in query_job.result()]  # Transformation des résultats en liste de dictionnaires
    display = display_data(result_data, "events/search", page)
    
    return display # Retour des résultats au format JSON


# Route pour rechercher des événements en fonction du nom d'artiste
@router.get("/events/artist/{artistName}")
def event_artist(
    artistName: str,
    page: int = 1
):
    # Fonction pour mesurer la similarité entre deux chaînes de caractères (pour les correspondances approximatives)
    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()

    # Normalisation du nom d'artiste (en minuscules et sans espaces)
    artistName = artistName.lower().replace(" ", "")

    # Requête pour récupérer tous les noms d'artistes de la base de données
    query = f"""
        SELECT artistName FROM {data}
    """
    
    query_job = client.query(query)
    all_artists = [row["artistName"] for row in query_job.result()]  # Liste de tous les artistes
    
    # Recherche du meilleur match basé sur la similarité
    best_match = max(all_artists, key=lambda x: similar(x.lower().replace(" ", ""), artistName))
    
    # Si la similarité est inférieure à un seuil, on renvoie une erreur
    if similar(best_match.lower().replace(" ", ""), artistName) < 0.8:
        return {"error": "No close match found for the artist name."}

    # Requête pour récupérer tous les événements associés au meilleur match trouvé
    query = f"""
        SELECT * FROM {data}
        WHERE LOWER(REPLACE(artistName, " ", "")) = "{best_match.lower().replace(" ", "")}"
    """
    
    query_job = client.query(query)
    result_data = [dict(row) for row in query_job.result()]  # Résultats de la recherche par artiste
    display = display_data(result_data, "events/artist/{artistName}", page)
    
    return display # Retour des résultats au format JSON

# Route pour obtenir des statistiques sur les événements par jour de la semaine (nombre d'événements par jour)
@router.get("/events/by-day-of-week")
async def get_events_by_day_of_week(page: int = 1, week: str = None):
    query = f"""select * 
    from `dataset_groupe_4.enrich`
    """
    
    # Exécutez la requête
    query_job = client.query(query)
    
    # Récupérez les résultats
    df = query_job.result().to_dataframe()
    df['startsAt'] = pd.to_datetime(df['startsAt'])
    df['day_of_week'] = df['startsAt'].dt.day_name()
    df['week'] = df['startsAt'].dt.isocalendar().week
    if week:
        df = df.query(f"week == {week}")
    df_day_of_week = df.groupby('day_of_week')["day_of_week"].count()
    
    # convert to dictionary
    data = df_day_of_week.to_dict()
     
    return data


# Route pour obtenir des statistiques sur les événements par lieu (nombre d'événements par lieu)
@router.get("/events/by-venue")
def by_venue(page : int = 1):
    # Requête SQL pour obtenir le nombre d'événements par lieu et des statistiques globales
    statistics_query = f"""
        WITH event_counts AS (
            SELECT 
                venueName, 
                COUNT(*) AS eventCount
            FROM {data}
            GROUP BY venueName
        ),
        global_stats AS (
            SELECT
                ROUND(AVG(eventCount),1) AS avgCount,
                APPROX_QUANTILES(eventCount, 100)[OFFSET(50)] AS medianCount,
                MIN(eventCount) AS minCount,
                MAX(eventCount) AS maxCount,
                SUM(eventCount) AS totalCount
            FROM event_counts
        )
        SELECT 
            ec.venueName,
            ec.eventCount,
            gs.avgCount,
            gs.medianCount,
            gs.minCount,
            gs.maxCount,
            gs.totalCount
        FROM event_counts ec
        CROSS JOIN global_stats gs
    """
    # Exécution de la requête et récupération des résultats
    query_job = client.query(statistics_query)
    result_data = [dict(row) for row in query_job.result()]  # Résultats des statistiques par lieu
    display = display_data(result_data, "events/by-venue", page)
    
    return display # Retour des résultats au format JSON

# Route pour comparer les événements en streaming et en personne
@router.get("/events/streaming-vs-in-person")
def streaming_vs_in_person():
    # Requête SQL pour compter les événements par type (streaming ou en personne)
    query = f"""
        SELECT 
            streamingEvent,
            COUNT(*) AS eventCount
        FROM {data}
        GROUP BY streamingEvent
    """
    query_job = client.query(query)
    result_data = [dict(row) for row in query_job.result()]  # Résultats des événements par type
    return result_data  # Retour des résultats


# Route pour prédire la popularité des événements basés sur l'artiste et le lieu
@router.get("/events/is_popular")
def is_popular(
    artistName: Optional[str] = None,
    venueName: Optional[str] = None
): 
    # Liste des conditions pour la requête SQL
    conditions = []
    if artistName:
        conditions.append(f'artistName = "{artistName}"')
    if venueName:
        conditions.append(f'venueName = "{venueName}"')

    # Si aucun paramètre n'est fourni, on renvoie une erreur
    if not venueName and not artistName:
        return {"error": "Please provide either an artist name or a venue name."}
    
    # Création de la clause WHERE en fonction des conditions
    where_clause = " AND ".join(conditions) if conditions else "1=1"

    # Requête pour récupérer les événements associés à l'artiste ou au lieu spécifié
    query = f"""
        SELECT venueName, venueType, Weekend, duration, international, artistName
        FROM {data}
        WHERE {where_clause}
    """
    
    query_job = client.query(query)
    result_data = [dict(row) for row in query_job.result()]  # Résultats des événements

    # Chargement du modèle et des encodeurs pour la prédiction
    model = load("model/random_forest_popularity_model.pkl")
    venueName_encoder = load("model/venueName_encoder.pkl")
    venueType_encoder = load("model/venueType_encoder.pkl")

    df = pd.DataFrame(result_data)  # Conversion des résultats en DataFrame

    # Transformation des colonnes avant la prédiction
    df["Original_venueName"] = df["venueName"].copy()
    df["venueName"] = venueName_encoder.transform(df["venueName"])
    df["venueType"] = venueType_encoder.transform(df["venueType"])

    # Prédiction de la popularité des événements
    df["predicted_popularity"] = model.predict(df.drop(columns=["Original_venueName", "artistName"]))

    # Retourner les résultats avec les prédictions sous forme de liste de dictionnaires
    events_with_predictions = df[["Original_venueName", "artistName", "predicted_popularity"]].to_dict(orient="records")

    return {"events": events_with_predictions}

@router.get("/events/popular_event_these_days")
async def popular_event_these_days(
    startdate: str,
    endate: Optional[str] = None,
    page: int = 1
):
    data = "`dataset_groupe_4.enrich`"
    if endate is None:
        endate = date.today().strftime("%Y-%m-%d")

    # Requête SQL pour obtenir les événements entre deux dates
    query = f"""
        SELECT venueName, venueType, Weekend, duration, international, artistName, startsAt
        FROM {data}
        WHERE startsAt BETWEEN '{startdate}T00:00:00' AND '{endate}T23:59:59'
    """
    
    # Exécution de la requête SQL
    query_job = client.query(query)
    result_data = [dict(row) for row in query_job.result()]  # Résultats des événements

    # Chargement du modèle et des encodeurs pour la prédiction
    model = load("model/random_forest_popularity_model.pkl")
    venueName_encoder = load("model/venueName_encoder.pkl")

    
    venueType_encoder = load("model/venueType_encoder.pkl")

    # Conversion des résultats en DataFrame
    df = pd.DataFrame(result_data)
    df = df.dropna(subset=["venueType"])

    # Transformation des colonnes avant la prédiction
    df["Original_venueName"] = df["venueName"].copy()
    df["venueName"] = venueName_encoder.transform(df["venueName"])
    df["venueType"] = venueType_encoder.transform(df["venueType"])

    # Prédiction de la popularité des événements
    df["predicted_popularity"] = model.predict(
        df.drop(columns=["Original_venueName", "artistName", "startsAt"])
    )

    # Filtrer les événements populaires
    popular_events = df[df["predicted_popularity"] == "Populaire"]

    # Retourner les résultats avec les prédictions sous forme de liste de dictionnaires
    events_with_predictions = popular_events[
        ["Original_venueName", "artistName", "predicted_popularity", "startsAt"]
    ].to_dict(orient="records")

    display = display_data(events_with_predictions, "events/popular_event_these_days", page)
    return display


if __name__ == "__main__":
    pass

    