import os
import pandas as pd
import pickle
from functools import reduce

def load_data_events(pkl_file): 
    with open(pkl_file, 'rb') as f:
        concerts = pickle.load(f)
    df = pd.DataFrame(concerts)
    df = df.loc[:, ~df.apply(lambda col: col.astype(str).str.startswith('https://')).any()]
    return df


def load_all_events(): 
    repertory = 'data'
    pkl_files = [os.path.join(repertory, f) for f in os.listdir(repertory) if f.endswith('.pkl')]
    dfs = list(map(load_data_events, pkl_files))
    df = reduce(lambda df1, df2: pd.concat([df1, df2]), dfs)
    return df 

if '__main__' == __name__:
   df = load_all_events()
   df.to_csv('events.csv')
   print(df.head())
   print(df.columns)