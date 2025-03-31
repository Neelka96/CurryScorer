# Import depdencies
import pandas as pd
import requests
import io
import datetime as dt
from tenacity import retry, stop_after_attempt, wait_exponential

# Bring in custom logger
from Core.log_config import init_log
log = init_log(__name__)


def get_df(
        url: str
        ,params: dict[str, int | str]
        ,config: dict[str, int | str]
        ) -> pd.DataFrame:
    '''Inner wrapper for requests to Socrata without SODA package using tenacity for retries.

    Args:
        url (str): Base URL for call.
        params (dict[str, int  |  str]): Parameters for call.
        config (dict[str, int  |  str]): Config dictionary for API calls.

    Returns:
        pd.DataFrame: Requested data converted to CSV style.
    '''
    log.debug('Call to get_df() outer wrapper made.')
    @retry(stop = stop_after_attempt(config['RETRY']), wait = wait_exponential(multiplier = 1, min = config['DELAY'], max = 30))  # Loops for the number of retries set using retry decorator
    def get_df_with_retry(url, params, config):
        log.debug('Entering tenacity retry loop.')
        try:
            log.debug('Sending API request.')
            response = requests.get(url, params, timeout = config['TIMEOUT'])
            response.raise_for_status() # Raise on bad response status
        except requests.exceptions.RequestException:
            log.warning('Request exception error.', exc_info = True)
            raise
        log.debug('Successful API call. Returning DataFrame.')
        return pd.read_csv(io.StringIO(response.content.decode('utf-8')))   # Using io.StringIO to create pseudo CSV file for reading
    
    return get_df_with_retry(url, params, config)



def where_filter(years: int = None) -> str:
    '''Filtering to reduce overhead data overhead during API call.

    Args:
        years (int, optional): Defaults to None.

    Returns:
        str: `$WHERE` clause string filter for parameters.
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


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')