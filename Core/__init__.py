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
def Main_Ops():
    '''
    Runs main extraction and transformations methods that occur each time on initialization or updates. APIs are called if needed with properties from config file.
    '''
    # Extract main dataset from API
    dohmh_df = E.extraction('dohmh', C.NYC_OPEN_KEY)

    # Get mappings for boro and cuisine dictionaries
    boro_map = T.map_borough()
    cuisine_map = T.map_cuisine()

    # Get Fast Food names list
    fastfood_names = etl.get_fastfoods(C.NYC_OPEN_KEY).to_numpy().tolist()

    # Clean, correct, organize, and normalize using mappings
    clean_df = T.transformation(dohmh_df, fastfood_names, boro_map, cuisine_map)

    # ---------------------------------------------------------------------------------------------------------
    # Grab population data from extraction (FOR NOW TESTING IS DONE THROUGH CSV)
    population_dict = pd.read_csv(C.POPULATION_CLEAN).set_index('borough')['population'].to_dict()
    # ---------------------------------------------------------------------------------------------------------

    return clean_df, population_dict, boro_map, cuisine_map


# Init database when it doesn't exist
def init_db() -> int:
    '''
    Calls APIs as needed (most likely all), performs ETL, creates DataBase Schema, and loads all tables from scratch.

    Returns:
        int: Returns 0 on a successful run.
    '''
    # Run Core ETL Operations and grab all returns for forging
    main_df, population_dict, boro_map, cuisine_map = Main_Ops()
    
    # Forge reference tables using mappings
    boro_df = T.forge_boroughs(boro_map, population_dict)
    cuisine_df = T.forge_cuisines(cuisine_map)

    # Create tables with enforced schema, in proper order
    Base.metadata.create_all(engine)
    L.freshTable(Session, Boroughs, boro_df)
    L.freshTable(Session, Cuisines, cuisine_df)
    L.freshTable(Session, Restaurants, main_df)
    return 0


# Runs to update db, doesn't recreate reference tables
def update_db() -> int:
    '''
    Runs Core_ETL_Ops to update Restaurants and Boroughs Tables - only calls APIs as needed in order to update Restaurants and the population in Boroughs.

    Returns:
        int: Returns 0 on a successful run.
    '''
    # Run Core ETL Operations and only grab the cleaned restaurant df
    main_df, population_dict, _, _ = Main_Ops()

    # Update Restaurants Table
    L.freshTable(Session, Restaurants, main_df)

    # Update the Boroughs Table
    L.updatePopulation(Session, Boroughs, population_dict)
    return 0


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')