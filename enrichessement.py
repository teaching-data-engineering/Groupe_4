import requests
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('data/events.csv')
#print((pd.to_datetime(df['startsAt'])).datetime.datetime.weekday())

# add a columns to the dataframe for week day, day of the week
df['startsAt'] = pd.to_datetime(df['startsAt'])
df['weekday'] = df['startsAt'].dt.weekday
df['day_of_week'] = df['startsAt'].dt.day_name()
df['endsAt'] = pd.to_datetime(df['endsAt'])

# Ajout du nombre de jours avant le concert
df['days_before'] = (df['startsAt'] - pd.to_datetime(datetime.datetime.now()))


print(df[["day_of_week", "endsAt", "startsAt", "weekday", "days_before"]].head())

# visualisation du nombre d'artistes en fontion du jour de la semaine
df.groupby('day_of_week').size().plot(kind='bar')
plt.title('Number of artists per day of the week')
plt.ylabel('Number of artists')
plt.xlabel('Day of the week')
#plt.show()




