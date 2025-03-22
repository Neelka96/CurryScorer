import pandas as pd
from time import sleep

from Assets.etl import extract as E
from . import transform as T
from Assets import config as C

# Larger Abstractions

def map_borough() -> dict:
    '''
    Wrapper for `create_dict()` to create a borough dictionary with necessary static list.
    '''
    try:
        # Utilizes constant BOROUGHS from config to call create_dict()
        return T.create_dict(C.BOROUGHS, lambda num: f'B{num}')
    except Exception as e:
        raise RuntimeError(f'Could not create dictionary from borough list: {e}')


def map_cuisine() -> dict:
    '''
    Wrapper for `create_dict()` to create cuisine dictionary using derived ethnic cuisine list.
    '''
    try:
        # Utilizes constant CUISINES from config file to call create_dict()
        return T.create_dict(C.CUISINES, lambda num: f'C{num}')
    except Exception as e:
        raise RuntimeError(f'Could not create dictionary from cuisines list: {e}')


def forge_boroughs(map: dict[str, str]) -> pd.DataFrame:
    '''
    Wrapper for create_ref_table - Creates new Boroughs table (if needed) through dictionary mappings.
    '''
    # Call and return a created reference table for boroughs using set variables
    return T.create_ref_table(map, 'borough', 'borough_id')


def forge_cuisines(map: dict[str, str]) -> pd.DataFrame:
    '''
    Wrapper for create_ref_table - Creates new Cuisines table (if needed) through dictionary mappings.
    '''
    # Call and return a created reference table for boroughs using set variables
    return T.create_ref_table(map, 'cuisine', 'cuisine_id')


def fastfood_csv() -> pd.DataFrame:
    '''
    Retrieves data from fastfood.csv if it exists, and calls 
    extraction method to request the API if it doesn't.
    '''
    try:
        if C.FASTFOOD_CSV.exists():
            return pd.read_csv(C.FASTFOOD_CSV)
        else:
            sleep(C.SLEEP_TIME)
            df = E.extraction('fast_food')
            df.to_csv(C.FASTFOOD_CSV)
            return df
    except Exception as e:
        raise RuntimeError(f'Could not extract fast_food df: {e}')


def transformation(
        df: pd.DataFrame
        ,boro_dict: dict[str, str]
        ,cuisine_dict: dict[str, str]
        ) -> pd.DataFrame:
    
    # Clean df by dropping fastfood names and keeping only restaurants with ethnic cuisines
    df = T.clean_df(df, fastfood_csv().values.tolist(), C.CUISINES)  # Clean df using new dictionaries

    # Normalize the table twice, once for each reference table
    df = T.normalizeTable(df, boro_dict, 'borough', 'borough_id')
    return T.normalizeTable(df, cuisine_dict, 'cuisine', 'cuisine_id')


if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')