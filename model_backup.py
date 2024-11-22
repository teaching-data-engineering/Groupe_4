from load_data import load_all_events
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
import joblib
import enrich

# Charger les données
df = load_all_events()
df = enrich.process_data(df,ask_gemini= False)

# Créer des catégories pour 'rsvpCount' en se basant sur les quantiles
df['popularity'] = pd.qcut(df['rsvpCountInt'], q=2, labels=['peu populaire', 'Populaire'], duplicates='drop')

# Sélectionner les colonnes pertinentes
features = ['venueName', 'venueType', 'Weekend', 'duration', 'international']
X = df[features]
y = df['popularity']
# Encoder les variables catégorielles
le_venueName = LabelEncoder()
le_venueType = LabelEncoder()

X['venueName'] = le_venueName.fit_transform(X['venueName'])
X['venueType'] = le_venueType.fit_transform(X['venueType'])
X['Weekend'] = X['Weekend'].astype(int)  # Assurez-vous que 'weekend' est numérique
X['international'] = X['international'].astype(int)  # Assurez-vous que 'international' est numérique

# Diviser les données en jeu d'entraînement et de test (hold-out)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Créer le modèle Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42)

# Entraîner le modèle
rf.fit(X_train, y_train)

# Prédictions et évaluation
y_pred = rf.predict(X_test)
print(classification_report(y_test, y_pred))

# Enregistrer le modèle
joblib.dump(rf, 'model/random_forest_popularity_model.pkl')

# Enregistrer les encodeurs pour pouvoir transformer les nouvelles données
joblib.dump(le_venueName, 'model/venueName_encoder.pkl')
joblib.dump(le_venueType, 'model/venueType_encoder.pkl')

if __name__ == '__main__':

    print("Modèle entraîné et enregistré avec succès !")
    print("Encoders enregistrés avec succès !")


