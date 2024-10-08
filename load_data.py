import pandas as pd
import pickle


def load_data_events(pkl_file): 
    with open('concerts.pkl', 'rb') as f:
        concerts = pickle.load(f)
    df = pd.DataFrame(concerts)
    df = df.loc[:, ~df.apply(lambda col: col.astype(str).str.startswith('https://')).any()]
    return df

if '__main__' == __name__:
    df = load_data_events('concerts.pkl')
    print(df.head())