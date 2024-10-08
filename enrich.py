import os
import json
import google.generativeai as genai
from load_data import load_all_events

# Configuration de l'API Gemini
with open('credentials/api_key.txt', 'r') as file:
    api_key = file.read().strip()

os.environ["GEMINI_API_KEY"] = api_key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_nationality_artists(artists):
    # Configuration du modèle
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )
    
    # Création de la session de chat
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    f"Je vais te fournir une liste d'artistes internationaux qui vont se produire à Berlin. "
                    f"Pour chaque artiste, indique leur nationalité. Pour cela renvoie moi un Json avec en clé "
                    f"le nom de l'artiste et en valeur sa nationalité identifiée par un code ISO. "
                    f"Si tu ne connais pas la nationalité d'un artiste, écris 'NA'. Voici la liste des artistes : {artists}"
                ],
            },
        ]
    )
    
    # Envoi de la requête et récupération de la réponse
    response = chat_session.send_message("Génère le JSON des nationalités pour ces artistes.")
    
    # Parsing de la réponse JSON
    try:
        nationalities = json.loads(response.text)
    except json.JSONDecodeError:
        print("Erreur : La réponse n'est pas un JSON valide.")
        nationalities = {}
    
    return nationalities

def get_category_venues(venues):
    # Configuration du modèle
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )
    
    # Création de la session de chat
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    f"Je vais te fournir une liste d'endroit à Berlin. "
                    f"Pour chaque endroit, indique sa catégorie, si c'est un bar, une salle de concert, un festival ou autre chose, si tu ne sais pas renvoie NA."
                    f"Voici la liste des salles : {venues}"
                ],
            },
        ]
    )

    # Envoi de la requête et récupération de la réponse
    response = chat_session.send_message("Génère le JSON des catégories pour ces salles.")

    # Parsing de la réponse JSON
    try:
        capacities = json.loads(response.text)
    except json.JSONDecodeError:
        print("Erreur : La réponse n'est pas un JSON valide.")
        capacities = {}

    return capacities

def process_data(df,ask_gemini = False):
    # Récupération des artistes et des salles
    artists = list(set(df['artistName']))
    venues = set(df['venueName'])

    # Récupération des nationalités
    if ask_gemini:
        nationalities = get_nationality_artists(artists)
        capacities = get_category_venues(venues)

        with open('metadata/artist_nationalities.json', 'w') as f:
            json.dump(nationalities, f, indent=2)

        with open('metadata/venue_capacities.json', 'w') as f:
            json.dump(capacities, f, indent=2)

    else:
        with open('metadata/artist_nationalities.json', 'r') as f:
            nationalities = json.load(f)
        with open('metadata/venue_capacities.json', 'r') as f:
            capacities = json.load(f)

    # Reconstruction des données
    df['nationality'] = df['artistName'].map(nationalities)
    df['venueType'] = df['venueName'].map(capacities)

    # Binarisation de la nationalité
    df['international'] = df['nationality'].apply(lambda x: x != 'DE') 

    return df 

# Exemple d'utilisation
if __name__ == '__main__':
    df = load_all_events()
    process_data(df,ask_gemini= False)