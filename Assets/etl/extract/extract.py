# Import depdencies
import pandas as pd
import requests
import io
import datetime as dt
from time import sleep

# Import package and subpackage requirements for core building
import config as C

def get_df(
        url: str
        ,params: dict[str, str] = None
        ,retries: int = C.API_RETRY
        ,delay: int = C.API_DELAY
        ,timeout_req: int = C. API_TIMEOUT
        ) -> pd.DataFrame:
    '''
    Fetches data from the specified URL and converts it into a pandas DataFrame. Loops for API request retries if a request fails. Default parameters are in place handling request failure.

    Args:
        url (str): The URL to fetch data from.
        params (dict, optional): Query parameters for the API request.
        retries (int, optional): Max retries allowed per API request.
        delay (int, optional): Seconds to wait between retries of API request.
        timeout_req (int, optional): Seconds allowed before timing out API request.

    Returns:
        pd.DataFrame: A DataFrame containing the data retrieved from the API.

    Raises:
        requests.exceptions.Timeout: If the request times out after retries.
        requests.exceptions.RequestException: For other request-related errors.
    '''
    # Loops for the number of retries set
    for attempt in range(1, retries + 1):
        # Tries to call API using socrata (SODA) querying
        try:
            # Times out after set number of seconds
            response = requests.get(url, params, timeout = timeout_req)
            response.raise_for_status()     # Raise on bad response status

            # Print successful API return with attempt number
            print(f'Successful API request on attempt {attempt}.')
            
            break   # Break loop early on success
        
        # If it can't retrieve data from timeout retry after delay
        except requests.exceptions.Timeout as e:
            print(f'Timeout on API attempt {attempt}: {e}')

            # Checks if retries is at limit
            if attempt < retries:
                print(f'Retrying in {delay} seconds.')
                sleep(delay)

            # If it is exit with failure.
            else:
                raise e('Max retries reaches. Request failed.')
        
        # If there was an error besides timeout, exit function early with error
        except requests.exceptions.RequestException as e:
            raise e(f'Major error encountered. Request failed.')
        
    # Using io.StringIO to create pseudo CSV file for reading
    csv = io.StringIO(response.content.decode('utf-8'))
    return pd.read_csv(csv)


def where_filter(years: int = C.INSPECTION_CUTOFF) -> str:
    '''
    Builds a `$where` filter for a Socrata SODA query of the `dohmh` dataset.

    Args:
        years (int, optional): The number of years by which to filter the data.

    Returns:
        str: A string representing the `$where` clause for the query.
    '''
    # Build filter for date, to cutoff on a certain number of years (default 2)
    dateLimit = (dt.datetime.now() - dt.timedelta(days = years * 365)).isoformat()
    filter_dt = f'inspection_date > "{dateLimit}"'

    # Build filter for non-null cuisine, latitude, or longitude
    notNull = 'IS NOT NULL'
    filter_NA = \
        f'cuisine {notNull} AND lat {notNull} AND lng {notNull}'
    
    # Return string ready $where clause
    return f'{filter_dt} AND {filter_NA}'



if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')