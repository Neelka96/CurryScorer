import pandas as pd
from pathlib import Path

from . import extract as E
import config as C 


def extraction(dataSet: str | Path) -> pd.DataFrame:
    # Conditional switch for 2 datasets
    if dataSet == 'dohmh':
    # Build select statement with aliases
        select = (
            'camis AS id,'
            'dba AS name,'
            'boro AS borough,'
            'cuisine_description AS cuisine,'
            'inspection_date,'
            'latitude AS lat,'
            'longitude AS lng'
        )
        # Parameters to send with API Call
        params = {
            '$select': select,
            '$where': E.where_filter(C.INSPECTION_CUTOFF),
            '$limit': C.ROW_LIMIT
        }
        url = 'https://data.cityofnewyork.us/resource/43nn-pn8j.csv'

    elif dataSet == 'fast_food':
        # Build select statement with aliases
        select = 'distinct restaurant AS name,'

        # Parameters to send with API Call
        params = {
            '$select': select,
            '$limit': C.ROW_LIMIT
        }
        url = 'https://data.cityofnewyork.us/resource/qgc5-ecnb.csv'

    elif dataSet == 'testing':
        return pd.read_csv(C.DOHMH_CLEAN)

    # Return extracted and file-formatted data
    return E.get_df(url, params)



if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')