# Import Directory Modules for Core Building
from . import etl
from .etl import extract as E
from .etl import transform as T
from .etl import load as L
from .backend.database import Session, engine, Base, Boroughs, Cuisines, Restaurants

# ---------------------
# FOR TESTING PURPOSES:
import config as C
import pandas as pd
# ---------------------


# Core Abstractions

# Main Extraction and Transformation Operations
def Main_Ops(nyc_open_key: str = None):
    '''
    Runs main extraction and transformations methods that occur each time on initialization or updates. APIs are called if needed with properties from config file.

    Args:
        nyc_open_key (str): The New York City Open (NYC Open) API Key to be used for accessing the datasets.

    Returns:
        Multiple returns, working on repairing return docstrings.
    '''
    # Extract main dataset from API
    print('Attempting to request Department of Health & Mental Hygiene Dataset from NYC Open...')
    dohmh_df = E.extraction('dohmh', nyc_open_key)
    print('Main dataset extracted!\n')


    # Get mappings for boro and cuisine dictionaries
    print('Mapping Boroughs and Cuisines into dictionaries for referencing...')
    boro_map = T.map_borough()
    cuisine_map = T.map_cuisine()
    print('Boroughs and Cuisines references mapped!\n')


    # Get Fast Food names list
    print('Retrieving list of fast food names to remove...')
    fastfood_names = etl.get_fastfoods(nyc_open_key)['name'].to_list()
    print('Names retrieved!\n')


    # Clean, correct, organize, and normalize using mappings
    print('Attempting to transform main restaurants dataframe using acquired data...')
    clean_df = T.transformation(dohmh_df, fastfood_names, boro_map, cuisine_map)
    print('Transformation completed!\n')


    # ---------------------------------------------------------------------------------------------------------
    # Grab population data from extraction (FOR NOW TESTING IS DONE THROUGH CSV)
    print('Grabbing population data from CSV and preparing for dictionary formatting for mapping')
    population_dict = pd.read_csv(C.POPULATION_CLEAN).set_index('borough')['population'].to_dict()
    print('Population dictionary created!\n')
    # ---------------------------------------------------------------------------------------------------------

    return clean_df, population_dict, boro_map, cuisine_map


# Init database when it doesn't exist
def init_db(nyc_open_key: str = None) -> int:
    '''
    Calls APIs as needed (most likely all), performs ETL, creates DataBase Schema, and loads all tables from scratch.

    Args:
        nyc_open_key (str): The New York City Open (NYC Open) API Key to be used for accessing the datasets.

    Returns:
        int: Returns 0 on a successful run.
    '''
    # Run Core ETL Operations and grab all returns for forging
    print(
        'Running Main Operations...'
        '--------------------------\n'
    )
    main_df, population_dict, boro_map, cuisine_map = Main_Ops(nyc_open_key)
    print(
        '\n------------------------------------'
        'Successful run of main operations!\n'
    )
    
    # Forge reference tables using mappings
    print('Forging Boroughs and Cuisines DataFrames...')
    boro_df = T.forge_boroughs(boro_map, population_dict)   # Should probably implement a join vs map in the forging if it's faster
    cuisine_df = T.forge_cuisines(cuisine_map)
    print('DataFrames successfully forged!\n')

    # Create tables with enforced schema, in proper order
    print('Attempting to create Boroughs, Cuisines, and Restaurants Tables (in that order)...')
    Base.metadata.create_all(engine)
    L.freshTable(Session, Boroughs, boro_df)
    L.freshTable(Session, Cuisines, cuisine_df)
    L.freshTable(Session, Restaurants, main_df)
    print('SQLite Tables created (along with metadata/schema)!\n')
    return 0


# Runs to update db, doesn't recreate reference tables
def update_db(nyc_open_key: str = None) -> int:
    '''
    Runs Core_ETL_Ops to update Restaurants and Boroughs Tables - only calls APIs as needed in order to update Restaurants and the population in Boroughs.

    Args:
        nyc_open_key (str): The New York City Open (NYC Open) API Key to be used for accessing the datasets.
        
    Returns:
        int: Returns 0 on a successful run.
    '''
    # Run Core ETL Operations and only grab the cleaned restaurant df
    print(
        'Running Main Operations...'
        '--------------------------\n'
    )
    main_df, population_dict, _, _ = Main_Ops(nyc_open_key)
    print(
        '\n------------------------------------'
        'Successful run of main operations!\n'
    )

    # Update Restaurants Table
    print('Recreating just restaurants from scratch...')
    L.freshTable(Session, Restaurants, main_df)
    print('Restaurants updated!\n')

    # Update the Boroughs Table
    print('Updating the population in Boroughs...')
    L.updatePopulation(Session, Boroughs, population_dict)
    print('Population updated!\n')
    return 0


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')