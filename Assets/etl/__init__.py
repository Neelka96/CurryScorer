# Import Directory Modules for Core Building
from . import extract as E
from . import transform as T
from . import load as L
from . import database as db

# FOR TESTING PURPOSES:
import config as C
import pandas as pd
# ---------------------

# Init database when it doesn't exist
def init_db():
    '''
    Creates database from scratch along with all reference tables and calls API for fresh data.
    '''
    # Extract main dataset from API
    dohmh_df = E.extraction('dohmh')

    # Get mappings for boro and cuisine dictionaries
    boro_map = T.map_borough()
    cuisine_map = T.map_cuisine()

    # Clean, correct, organize, and normalize using mappings
    clean_df = T.transformation(dohmh_df, boro_map, cuisine_map)

    # Grab population data from extraction (FOR NOW TESTING IS DONE THROUGH CSV)
    population_dict = pd.read_csv(C.POPULATION_CLEAN).set_index('borough', drop = True).to_dict()

    # Forge reference tables using mappings
    boro_df = T.forge_boroughs(boro_map, population_dict)
    cuisine_df = T.forge_cuisines(cuisine_map)

    # Create tables with enforced schema, in proper order
    db.Base.metadata.create_all(db.engine)
    L.newBoroughs(boro_df)
    L.newCuisines(cuisine_df)
    L.newRestauants(clean_df)
    return 0


def update_db():
    '''
    Calls API for updated restaurant dataset, doesn't touch reference tables.
    '''
    # Extract main dataset from API
    dohmh_df = E.extraction('dohmh')

    # Get mappings for boro and cuisine dictionaries
    boro_map = T.map_borough()
    cuisine_map = T.map_cuisine()

    # Clean, correct, organize, and normalize using mappings
    clean_df = T.transformation(dohmh_df, boro_map, cuisine_map)
    
    # Update restaurant table, no need to touch reference tables
    L.newRestauants(clean_df)
    return 0



if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')