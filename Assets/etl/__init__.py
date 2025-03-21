from . import extract as E
from . import transform as T
from . import load as L
from . import database as db

import pandas as pd
from pathlib import Path
from time import sleep

def fastfood_csv(url: Path = None) -> pd.DataFrame:
    try:
        if url.exists():
            return pd.read_csv(url)
        else:
            return E.extraction('fast_food')
    except Exception as e:
        raise RuntimeError(f'Could not extract fast_food df: {e}')

# Init database when it doesn't exist
def init_db(links: dict[Path]):
    # Sleeping between API calls
    dohmh_df = E.extraction('dohmh')
    sleep(10)
    drop_dict = {'name': fastfood_csv(links['fast_food']).values.tolist()}
    keep_dict = {'cuisine': T.grab_list(links['cuisine'])}
    clean_df, boro_df, cuisine_df = \
        T.transformation(
            dohmh_df
            ,links['cuisine']
            ,drop_dict
            ,keep_dict
            ,forge_all = True
        )
    db.Base.metadata.create_all(db.engine)
    L.newBoroughs(boro_df)
    L.newCuisines(cuisine_df)
    L.newRestauants(clean_df)
    return 0

def update_db(links: dict[Path]):
    # Sleeping between API calls
    dohmh_df = E.extraction('dohmh')
    sleep(5)
    drop_dict = {'name': fastfood_csv(links['fast_food']).values.tolist()}
    keep_dict = {'cuisine': T.grab_list(links['cuisine'])}
    clean_df = \
        T.transformation(
            dohmh_df
            ,links['cuisine']
            ,drop_dict
            ,keep_dict
        )
    db.Base.metadata.create_all(db.engine)
    L.newRestauants(clean_df)
    return 0

def testing_create(links: dict[Path], csv_path: Path):
    # Sleeping between API calls
    dohmh_df = E.extraction('testing', csv_path)
    sleep(10)
    drop_dict = {'name': fastfood_csv(links['fast_food']).values.tolist()}
    keep_dict = {'cuisine': T.grab_list(links['cuisine'])}
    clean_df, boro_df, cuisine_df = \
        T.transformation(
            dohmh_df
            ,links['cuisine']
            ,drop_dict
            ,keep_dict
            ,forge_all = True
        )
    db.Base.metadata.create_all(db.engine)
    L.newBoroughs(boro_df)
    L.newCuisines(cuisine_df)
    L.newRestauants(clean_df)
    return 0

def testing_update(links: dict[Path], csv_path: Path):
    # Sleeping between API calls
    dohmh_df = E.extraction('testing', csv_path)
    sleep(10)
    drop_dict = {'name': fastfood_csv(links['fast_food']).values.tolist()}
    keep_dict = {'cuisine': T.grab_list(links['cuisine'])}
    clean_df, boro_df, cuisine_df = \
        T.transformation(
            dohmh_df
            ,links['cuisine']
            ,drop_dict
            ,keep_dict
            ,forge_all = True
        )
    db.Base.metadata.create_all(db.engine)
    L.newRestauants(clean_df)

if __name__ == '__main__':
    print('Not scripted yet.')