import pandas as pd
import requests
import io
import datetime as dt
from pathlib import Path
from time import sleep

from Assets import config as C

def get_df(url: str, params: dict = None) -> pd.DataFrame:
    '''
    Warning: Not for public use.
    Calls API for starter data and decodes into a DataFrame.
    Retries API call based on constant from config file.
    '''
    for attempt in range(1, C.API_RETRY + 1):
        try:
            # API Call itself using socrata (SODA) querying
            response = requests.get(url, params, timeout = C.API_TIMEOUT)  # Timeout at 10 seconds for retry
            response.raise_for_status()     # Raise on bad response status
            print(f'Successful API request on attempt {attempt}.')
            break   # On successful retrieval break loop
        except requests.exceptions.Timeout as e:
            print(f'Timeout on API attempt {attempt}: {e}')
            if attempt < C.API_RETRY:
                print(f'Retrying in {C.API_DELAY} seconds.')
                sleep(C.API_DELAY)
            else:
                # Exiting on failure
                raise e('Max retries reaches. Request failed.')
        except requests.exceptions.RequestException as e:
            raise e(f'Major error encountered. Request failed.')
        
    # Using io.StringIO to create pseudo CSV file for reading
    csv = io.StringIO(response.content.decode('utf-8'))
    return pd.read_csv(csv)


def where_filter(numYears: int) -> str:
    '''
    Warning: Not for public use.
    Builds `$where` filter for Socrata SODA query of `dohmh` dataset.
    Returns string variant of `$where` clause
    '''
    # Build filters for date (default 2 years) and no nulls for cuisine, lat, or lng
    dateLimit = (dt.datetime.now() - dt.timedelta(days = numYears * 365)).isoformat()
    filter_dt = f'inspection_date > "{dateLimit}"'
    notNull = 'IS NOT NULL'
    filter_NA = \
        f'cuisine {notNull} AND lat {notNull} AND lng {notNull}'
    
    # Init full filters for API call with limit
    return f'{filter_dt} AND {filter_NA}'


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
            '$where': where_filter(C.INSPECTION_CUTOFF),
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
    return get_df(url, params)



if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')