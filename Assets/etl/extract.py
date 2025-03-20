import pandas as pd
import requests
import io
import datetime as dt


def get_df(url: str, params: dict = None) -> pd.DataFrame:
    # API Call itself using socrata (SODA) querying
    response = requests.get(url, params)

    # Using io.StringIO to create pseudo CSV file for reading
    csv = io.StringIO(response.content.decode('utf-8'))
    return pd.read_csv(csv)


def where_filter(numYears: int = 2) -> str:
    # Build filters for date (default 2 years) and no nulls for cuisine, lat, or lng
    dateLimit = (dt.datetime.now() - dt.timedelta(days = numYears * 365)).isoformat()
    filter_dt = f'inspection_date > "{dateLimit}"'
    notNull = 'IS NOT NULL'
    filter_NA = \
        f'cuisine {notNull} AND lat {notNull} AND lng {notNull}'
    
    # Init full filters for API call with limit
    return f'{filter_dt} AND {filter_NA}'


MAX_LIMIT = 200000
def extraction(dataSet: str, limit: str = MAX_LIMIT) -> pd.DataFrame:
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
            '$where': where_filter(),
            '$limit': limit
        }
        url = 'https://data.cityofnewyork.us/resource/43nn-pn8j.csv'

    elif dataSet == 'fast_food':
        # Build select statement with aliases
        select = (
            'restaurant AS name,'
            'Item_Name AS item,'
            'Food_Category AS cat'
        )
        # Parameters to send with API Call
        params = {
            '$select': select,
            '$limit': limit
        }
        url = 'https://data.cityofnewyork.us/resource/qgc5-ecnb.csv'

    # Return extracted and file-formatted data
    return get_df(url, params)



if __name__ == '__main__':
    print('Error: Not for direct execution.')