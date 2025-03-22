# Import modules for testing
from . import extract as E
from . import transform as T
from . import load as L
from . import database as db


def init_db():
    # Extract main dataset from CSV
    dohmh_df = E.extraction('testing')

    # Get mappings for boro and cuisine dictionaries
    boro_map = T.map_borough()
    cuisine_map = T.map_cuisine()

    # Clean, correct, organize, and normalize using mappings
    clean_df = T.transformation(dohmh_df, boro_map, cuisine_map)

    # Forge reference tables using mappings
    boro_df = T.forge_boroughs(boro_map)
    cuisine_df = T.forge_cuisines(cuisine_map)

    # Create tables with enforced schema, in proper order
    db.Base.metadata.create_all(db.engine)
    L.newBoroughs(boro_df)
    L.newCuisines(cuisine_df)
    L.newRestauants(clean_df)
    return 0


def update_db():
    # Extract main dataset from CSV
    dohmh_df = E.extraction('testing')

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