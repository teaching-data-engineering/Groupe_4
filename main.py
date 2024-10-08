import load_data 
import enrich
import scrapping 
import basing

def main():
    # Recuperation des données du site bandsintown
    scrapping.fetch_month()

    # Chargement de toutes les données dans un dataframe
    df = load_data.load_all_events()

    # Enrichissement des données
    df = enrich.process_data(df,ask_gemini= False)

    # Exportations des données enrichies sur GoogleQuery
    basing.func_basing(df)

if __name__ == '__main__':
    main()