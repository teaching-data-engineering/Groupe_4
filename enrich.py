import os
import json
from datetime import datetime
import google.generativeai as genai
from load_data import load_all_events

def load_json(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def get_gemini_data(items, prompt_template, model_name="gemini-1.5-flash"):
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
    }
    
    model = genai.GenerativeModel(model_name=model_name, generation_config=generation_config)
    chat_session = model.start_chat(history=[{"role": "user", "parts": [prompt_template.format(items=items)]}])
    response = chat_session.send_message("Génère le JSON pour ces éléments.")
    
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        print(f"Erreur : La réponse pour {items[:5]}... n'est pas un JSON valide.")
        return {}

import pandas as pd

def enrich_date_time(df):
    # Séparation de la date et de l'heure
    df[['date_start', 'hour_start']] = df['startsAt'].str.split('T', expand=True)
    
    # Conversion de la date en datetime
    df['date_start'] = pd.to_datetime(df['date_start'])
    
    # Détermination du weekend
    df['Weekend'] = df['date_start'].dt.dayofweek.isin([5, 6])

    df[['date_end','hour_end']] = df['endsAt'].str.split('T', expand=True)

    # Création de la colonne 'duration'
    df['duration'] = pd.to_datetime(df['endsAt']) - pd.to_datetime(df['startsAt'])   

    # Conversion de la durée en heures
    df['duration'] = df['duration'].dt.total_seconds() / 3600

    return df


def process_data(df, ask_gemini=False):
    artists = set(df['artistName'])
    venues = set(df['venueName'])

    nationalities = load_json('metadata/artist_nationalities.json')
    categories = load_json('metadata/venue_capacities.json')

    new_artists = list(artists - set(nationalities.keys()))
    new_venues = list(venues - set(categories.keys()))

    if ask_gemini and (new_artists or new_venues) :

        with open('credentials/api_key.txt', 'r') as file:
            os.environ["GEMINI_API_KEY"] = file.read().strip()
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])

        artist_prompt = ("Je vais te fournir une liste d'artistes internationaux qui vont se produire à Berlin. "
                         "Pour chaque artiste, indique leur nationalité. Pour cela renvoie moi un Json avec en clé "
                         "le nom de l'artiste et en valeur sa nationalité identifiée par un code ISO. "
                         "Si tu ne connais pas la nationalité d'un artiste, écris 'NA'. Voici la liste des artistes : {items}")
        
        venue_prompt = ("Je vais te fournir une liste d'endroits à Berlin. "
                        "Pour chaque endroit, indique sa catégorie, si c'est un bar, une salle de concert, un festival ou autre chose, si tu ne sais pas renvoie NA. "
                        "Voici la liste des salles : {items}")

        nationalities.update(get_gemini_data(new_artists, artist_prompt))
        categories.update(get_gemini_data(new_venues, venue_prompt))

        save_json('metadata/artist_nationalities.json', nationalities)
        save_json('metadata/venue_capacities.json', categories)

    # Creation des nouvelles colonnes 
    df['nationality'] = df['artistName'].map(nationalities)
    df['venueType'] = df['venueName'].map(categories)
    df['international'] = df['nationality'].apply(lambda x: x != 'DE')

    # Enrichissement sur les dates 
    df = enrich_date_time(df)

    return df 

if __name__ == '__main__':
    df = load_all_events()
    df = process_data(df, ask_gemini=False)
    df.to_csv('events.csv')