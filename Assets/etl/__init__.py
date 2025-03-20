import pandas as pd

import extract as E
import transform as T
import load as L
import database as db
from pathlib import Path
from time import sleep

#     # Build drop lists
#     if not csvPath.exists() or force_download:
#         drop_names = Extraction('fast_food')['name'].unique()
#         pd.Series({'name': drop_names}).to_csv(csvPath, header = True, index = False)

#     drop_names = pd.read_csv(csvPath)

def fastfood_csv(csv_path: Path = None) -> pd.DataFrame:
    if csv_path:
        url = csv_path
    else:
        url = Path('../data/clean/fastfood.csv')
    
    if url.exists():
        return pd.read_csv(url)
    else:
        return E.extraction('fast_food')
    

def init_db():
    # Sleeping between API calls
    dohmh_df = E.extraction('dohmh')
    sleep(10)
    CUISINE_URL = '../data/cuisine_bins/keep.txt'
    drop_dict = fastfood_csv().to_dict(orient = 'list')
    keep_dict = {'cuisine': T.grab_list(CUISINE_URL)}
    clean_df, boro_df, cuisine_df = \
        T.transformation(
            dohmh_df
            ,CUISINE_URL
            ,drop_dict
            ,keep_dict
            ,forge_all = True)
    db.Base.metadata.create_all(db.engine)
    


def update_db():
    pass


if __name__ == '__main__':
    print('Not scripted yet.')