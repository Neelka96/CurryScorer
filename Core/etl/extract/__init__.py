# Import dependencies
import pandas as pd

# Import package and subpackage requirements for core building
from . import extract as E
import config as C 

# # ------------------------------------------
# # !!!FOR TESTING DELETE LATER!!!
# from pathlib import Path
# # ------------------------------------------


# Extraction Abstractions

def extraction(
        dataSet: str
        ,api_key: str = None
        ,limit: int = C.ROW_LIMIT
        # ,test_csv_path: Path = C.DOHMH_CLEAN
        ) -> pd.DataFrame:
    '''
    Extracts data from a specified NYC Open dataset.

    Args:
        dataSet (str): The name of the dataset to extract or type of extraction.
        api_key (str): The API Key needed to make requests for given dataset.
        limit (int, optional): The number of rows to be returned by API request.

    Returns:
        pd.DataFrame: A DataFrame containing the extracted data.
    '''
    # Core extraction method used for all NYC Open Data API Calls
    # Encompasses query filtering and basic df creation

    # Cond'l: Get Restaurant Inspections dataset from NYC Department of Health and Mental Hygiene (NYC Open)
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
            '$select': select
            ,'$where': E.where_filter()
            ,'$limit': limit
            ,'$$app_token': api_key
        }
        # Endpoint for API Call
        url = 'https://data.cityofnewyork.us/resource/43nn-pn8j.csv'


    # Cond'l: Get NYC Common Fast Food dataset (NYC Open)
    elif dataSet == 'fast_food':
        # Build select statement with aliases
        select = 'distinct restaurant AS name'

        # Parameters to send with API Call
        params = {
            '$select': select
            ,'$limit': limit
            ,'$$app_token': api_key
        }
        # Endpoint for API Call
        url = 'https://data.cityofnewyork.us/resource/qgc5-ecnb.csv'

    
    # # -------------------------------------------
    # # !!!TESTING!!! FOR DELETION LATER
    # # GRABS DATA FROM CSV INSTEAD OF CALLING API
    # # ENDS FUNCTION EARLY
    # elif dataSet == 'testing':
    #     return pd.read_csv(test_csv_path)
    # # -------------------------------------------

    # Return extracted and file-formatted data
    return E.get_df(url, params, dataSet)


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')