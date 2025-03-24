# Import dependencies
import pandas as pd

# Import package and subpackage requirements for core building
from . import transform as T
import config as C


# Transformation Abstractions

def map_borough(borough_list: list[str] = C.BOROUGHS) -> dict[str, str]:
    '''
    Creates a dictionary mapping borough names to IDs.

    Args:
        borough_list (list[str], optional): A list of the 5 borough names in NYC to be mapped with IDs.

    Returns:
        dict[str, str]: A dictionary where keys are borough names and values are IDs.
    '''
    try:
        # Try to create a dictionary of reference IDs using a list of boroughs
        return T.create_dict(borough_list, lambda num: f'B{num}')
    except Exception as e:
        raise RuntimeError(f'Could not create dictionary from borough list: {e}')


def map_cuisine(cuisine_list: list[str] = C.CUISINES) -> dict[str, str]:
    '''
    Creates a dictionary mapping cuisine names to IDs.

    Args:
        cuisine_list (list[str], optional): A list of ethnic cuisines to be mapped with IDs.

    Returns:
        dict[str, str]: A dictionary where keys are cuisine names and values are IDs.
    '''
    try:
        # Try to create a dictionary of reference IDs using a list of ethnic cuisines
        return T.create_dict(cuisine_list, lambda num: f'C{num}')
    except Exception as e:
        raise RuntimeError(f'Could not create dictionary from cuisines list: {e}')


def forge_boroughs(
        id_map: dict[str, str]
        ,population_map: dict[str, int] = None
        ) -> pd.DataFrame:
    '''
    Creates a DataFrame for boroughs with optional population data.

    Args:
        id_map (dict[str, str]): A mapping of borough names to IDs.
        population_map (dict[str, int], optional): A mapping of borough names to population counts.

    Returns:
        pd.DataFrame: A DataFrame containing borough information, including population if provided.
    '''
    # Creates base Boroughs reference table
    boroughs_df = T.create_ref_table(id_map, 'borough')

    # If population is passed as argument it's added to the table through mappings with borough
    if population_map:
        boroughs_df['population'] = boroughs_df['borough'].map(population_map)
    
    # Returns set up borough df ready for db loading
    return boroughs_df


def forge_cuisines(id_map: dict[str, str]) -> pd.DataFrame:
    '''
    Creates a DataFrame for cuisines using a mapping of cuisine names to IDs.

    Args:
        id_map (dict[str, str]): A mapping of cuisine names to IDs.

    Returns:
        pd.DataFrame: A DataFrame containing cuisine information.
    '''
    # Returns set up cuisine df ready for db loading
    return T.create_ref_table(id_map, 'cuisine')


def transformation(
        df: pd.DataFrame
        ,fastfood_names: list
        ,boro_dict: dict[str, str]
        ,cuisine_dict: dict[str, str]
        ,target_cols: list[str] = ['borough', 'cuisine']
    ) -> pd.DataFrame:
    '''
    Transforms the main DataFrame by cleaning and normalizing it using reference mappings.

    Args:
        df (pd.DataFrame): The main DataFrame to transform.
        fastfood_names (list): The list of fast food restaurant names used to filter dataframe.
        boro_dict (dict[str, str]): A dictionary mapping borough names to IDs.
        cuisine_dict (dict[str, str]): A dictionary mapping cuisine names to IDs.
        target_cols (list[str], optional): Columns on which restaurant table is normalized.

    Returns:
        pd.DataFrame: The transformed DataFrame with normalized columns.
    '''
    # Calls cleaning on df using fast food restaurant names to drop rows, 
    # and keeping only ethnic cuisines defined
    df = T.clean_df(df, fastfood_names, cuisine_dict.keys())

    # Normalizes table twice, once for each reference table created (as dictated per created schema)
    df = T.normalizeTable(df, boro_dict, target_cols[0])
    return T.normalizeTable(df, cuisine_dict, target_cols[1])


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')