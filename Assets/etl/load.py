# Import dependencies
import pandas as pd
from sqlalchemy import Table, insert, delete

# # Import package and subpackage requirements for core building
from Assets.backend import database as db


def freshTable(TableClass: Table, df: pd.DataFrame) -> int:
    '''
    Deletes all existing data in the specified table and inserts new data from the provided DataFrame.

    Args:
        TableClass (Table): The SQLAlchemy table class to refresh.
        df (pd.DataFrame): The DataFrame containing the new data to insert.

    Returns:
        int: Returns 0 upon successful completion.

    Raises:
        RuntimeError: If the table cannot be refreshed due to an error.
    '''
    try:
        with db.Session() as session:
            session.execute(delete(TableClass))
            stmt = insert(TableClass)
            vals = df.to_dict('records')
            session.execute(stmt, vals)
            session.commit()
        return 0
    except Exception as e:
        raise RuntimeError(f'Could not build Fresh Table: {e}')


# Set Wrappers for access and writing using df
def newBoroughs(df: pd.DataFrame) -> int:
    '''
    Refreshes the `Boroughs` table with new data from the provided DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing borough data.

    Returns:
        int: Returns 0 upon successful completion.
    '''
    return freshTable(db.Boroughs, df)

def newCuisines(df: pd.DataFrame) -> int:
    '''
    Refreshes the `Cuisines` table with new data from the provided DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing cuisine data.

    Returns:
        int: Returns 0 upon successful completion.
    '''
    return freshTable(db.Cuisines, df)

def newRestauants(df: pd.DataFrame) -> int:
    '''
    Refreshes the `Restaurants` table with new data from the provided DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing restaurant data.

    Returns:
        int: Returns 0 upon successful completion.
    '''
    return freshTable(db.Restaurants, df)



if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')