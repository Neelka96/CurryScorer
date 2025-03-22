import pandas as pd
from typing import Callable
from time import sleep

from Assets.etl import extract as E
from Assets import config as C

# TRANSFORMATIONS

# Cleaner helper
def clean_helper(df: pd.DataFrame) -> pd.DataFrame:
    '''Recieves pandas DataFrame as input, returns de-duplicated and datetime type correct DataFrame.'''

    # Correcting date type --> datetime (doesn't need times or tz info)
    df['inspection_date'] = pd.to_datetime(df['inspection_date'])

    # Sort by inspection date for most recent dates then drop duplicate ids and keep most recent
    df = (df
            .sort_values('inspection_date', ascending = False)
            .drop_duplicates(subset = ['id'], keep = 'first'))

    # Reorder to correct columns
    df = df[
        ['id', 'name', 'borough', 'cuisine', 'inspection_date', 'lat', 'lng']
    ].reset_index(drop = True)

    return df


def clean_df(
        df: pd.DataFrame
        ,drop_dict: dict[str:list] = None
        ,keep_dict: dict[str:list] = None
    ) -> pd.DataFrame:
    '''Cleans pandas DataFrame by calling `clean_helper()` and dropping/keeping only objects passed into correctly designated arguments.'''

    # Calls clean_helper() on df to drop duplicates, sort columns, and correct datetime datetype
    try:
        df = clean_helper(df)
    except Exception as e:
        raise RuntimeError(f'Could not process clean_helper on df: {e}')

    # Performs filtering loops by dictionary passed into argument (if no arguments -> no filtering occurs)
    mask = pd.Series(True, index = df.index)
    if drop_dict:
        mask &= [~df[col].isin(dropList) for col, dropList in drop_dict.items()]
    if keep_dict:
        mask &= [df[col].isin(keepList) for col, keepList in keep_dict.items()]

    return df[mask]


def create_dict(ref_list: list, translation: Callable[[int], str]) -> dict:
    '''Takes in a reference list to create alias identifiers for, along with function used to map new aliases.'''

    # Dictionary comprehension used to apply function to each item as it's placed in dictionary
    norm_dict = {item : translation(num) for num, item in enumerate(ref_list, start = 1)}
    return norm_dict


def create_ref_table(
        mapping: dict[str, str]
        ,target_col: str
        ,new_col: str
    ) -> pd.DataFrame:
    '''
    Creates new reference table using a mapping, a column name, and adding `_id`.
    '''
    new_col = f'{target_col}_id'
    new_table = pd.DataFrame(
        {
            new_col: mapping.values(),
            target_col: mapping.keys()
        }
    )
    return new_table


def normalizeTable(
        denorm_df: pd.DataFrame
        ,mapping: dict[str, str]
        ,target_col: str
        ,new_col: str
    ) -> pd.DataFrame:
    '''Used to normalize main table with reference mappings on a target column.'''
    # Map dataframe target column values to dictionary containing new values
    denorm_df[target_col] = denorm_df[target_col].map(mapping)
    return denorm_df.rename(columns = {target_col: new_col})


# --------------------------------------------------------------------------------------------------------

# Larger Abstractions

def map_borough() -> dict:
    '''Wrapper for `create_dict()` to create a borough dictionary with necessary static list'''
    try:
        # Utilizes constant BOROUGHS from config to call create_dict()
        return create_dict(C.BOROUGHS, lambda num: f'B{num}')
    except Exception as e:
        raise RuntimeError(f'Could not create dictionary from borough list: {e}')


def map_cuisine() -> dict:
    '''Wrapper for `create_dict()` to create cuisine dictionary using derived ethnic cuisine list.'''
    try:
        # Utilizes constant CUISINES from config file to call create_dict()
        return create_dict(C.CUISINES, lambda num: f'C{num}')
    except Exception as e:
        raise RuntimeError(f'Could not create dictionary from cuisines list: {e}')


def forge_boroughs(map: dict[str, str]) -> pd.DataFrame:
    '''
    Wrapper for create_ref_table - Creates new Boroughs table (if needed) through dictionary mappings.
    '''
    # Call and return a created reference table for boroughs using set variables
    return create_ref_table(map, 'borough', 'borough_id')


def forge_cuisines(map: dict[str, str]) -> pd.DataFrame:
    '''
    Wrapper for create_ref_table - Creates new Cuisines table (if needed) through dictionary mappings.
    '''
    # Call and return a created reference table for boroughs using set variables
    return create_ref_table(map, 'cuisine', 'cuisine_id')


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
        ,mappings_list: list[dict[str, str]]
        ) -> pd.DataFrame:

    # Get mappings for both borough and cuisine using constants in config file
    boro_dict = mappings_list[0]
    cuisine_dict = mappings_list[1]

    # Clean df by dropping fastfood names and keeping only restaurants with ethnic cuisines
    fastFood_names = {'names': fastfood_csv().values.tolist()}  # Names of common fastfood restaurants
    ethnic_cuisines = {'cuisine': C.CUISINES}   # Names of derived ethnic cuisines
    df = clean_df(df, fastFood_names, ethnic_cuisines)  # Clean df using new dictionaries

    # Normalize the table twice, once for each reference table
    df = normalizeTable(df, boro_dict, 'borough', 'borough_id')
    return normalizeTable(df, cuisine_dict, 'cuisine', 'cuisine_id')


if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')