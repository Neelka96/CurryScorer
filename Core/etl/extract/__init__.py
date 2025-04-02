# Import dependencies
import pandas as pd
from time import sleep
from pathlib import Path

# Import subpackage requirements
from . import extract as E

# Bring in custom logger
from Core.log_config import init_log
log = init_log(__name__)


def extraction(
        dataSet: str
        ,config: dict[str, int | str]
        ) -> pd.DataFrame:
    '''Base extraction method for datasets in this project.

    Args:
        dataSet (str): Dataset requested.
        config (dict[str, int  |  str]): Config dictionary for API requests.

    Returns:
        pd.DataFrame: Extracted data.
    '''
    # Core extraction method used for all NYC Open Data API Calls
    # Encompasses query filtering and basic df creation
    log.debug('Grabbing config constants.')
    cutoff_years = config['DATE_CUTOFF']
    limit = config['ROW_LIMIT']
    key = config['KEY']

    # Cond'l: Get Restaurant Inspections dataset from NYC Department of Health and Mental Hygiene (NYC Open)
    if dataSet == 'dohmh':
        log.debug('DOHMH Dataset selected.')
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
            '$select': select
            ,'$where': E.where_filter(cutoff_years)
            ,'$limit': limit
            ,'$$app_token': key
        }
        # Endpoint for API Call
        url = 'https://data.cityofnewyork.us/resource/43nn-pn8j.csv'

    # Cond'l: Get NYC Common Fast Food dataset (NYC Open)
    elif dataSet == 'fastfood':
        log.debug('FastFoods Dataset selected.')
        # Build select statement with aliases
        select = 'distinct restaurant AS name'
        # Parameters to send with API Call
        params = {
            '$select': select
            ,'$limit': limit
            ,'$$app_token': key
        }
        # Endpoint for API Call
        url = 'https://data.cityofnewyork.us/resource/qgc5-ecnb.csv'

    # Return extracted and file-formatted data
    log.debug('Sending API request.')
    return E.get_df(url, params, config)


def get_addData(
        dataSet: str
        ,csv: Path
        ,api_config: dict[str, int | str]
        ) -> pd.DataFrame:
    '''Gets additional data after main source. Sleeps and validates CSV existance.

    Args:
        dataSet (str): Dataset requested.
        csv (Path): Where CSV lives or will live.
        api_config (dict[str, int  |  str]): Config dictionary for API requests.

    Returns:
        pd.DataFrame: New data requested.
    '''
    log.debug('Grabbing additional data.')
    sleeping = api_config['SLEEP']

    # Try to find or get fastfood data
    try:
        # Checks if csv path exists -> Returns df from csv
        if csv.exists():
            log.debug('CSV File already exists.')
            return pd.read_csv(csv)
        # Else extract a new csv (so sleep first between this and the first API call)
        else:
            # Save new df to prevent future API calls on this route and return df
            log.info(f'Sleeping between API calls for {sleeping} seconds...')
            sleep(sleeping)
            df = extraction(dataSet, api_config)
            df.to_csv(csv, header = True, index = False)
            return df
    except Exception:
        log.critical(f'Could not extract df.', exc_info = True)
        raise



# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')