# Import dependencies
import pandas as pd
from sqlalchemy import Table, select, insert, delete
from sqlalchemy.orm import Session, sessionmaker
from typing import Any

# Loading File

def freshTable(
        Session: sessionmaker[Session]
        ,tableClass: Table
        ,df: pd.DataFrame
        ) -> int:
    '''
    Deletes all existing data in the specified table and inserts new data from the provided DataFrame. 
    Only meant to be used the first time creating the reference tables and the main table. After that, only for the Restaurant table.

    Args:
        Session (sessionmaker[Session]): A session maker bound to an engine with configurations already, for accessing through the ORM Layer.
        tableClass (Table): The SQLAlchemy table class to create.
        df (pd.DataFrame): The DataFrame containing the new data to insert.

    Returns:
        int: Returns 0 upon successful run.

    Raises:
        RuntimeError: If the table cannot be refreshed due to an error.
    '''
    try:
        # Try to delete the table and insert it from scratch
        with Session() as session:
            session.execute(delete(tableClass))
            stmt = insert(tableClass)
            vals = df.to_dict('records')
            session.execute(stmt, vals)
            session.commit()
        return 0
    except Exception as e:
        raise RuntimeError(f'Could not build Fresh Table: {e}')


def updatePopulation(
        Session: sessionmaker[Session]
        ,tableClass: Table
        ,data_map: dict[str, Any]
        ) -> int:
    '''
    Updates the Borough's Table population column. Relies on passing of Table class even if it seems arbitrary.

    Args:
        Session (sessionmaker[Session]): A session maker bound to an engine with configurations already, for accessing through the ORM Layer.
        tableClass (Table): The SQLAlchemy Table class to modify. Always needs to be `Boroughs` Table.
        data_map (dict[str, Any]): A dictionary containing mappings of borough name to population value used for updating.
    
    Returns:
        int: Returns 0 upon successful run.
    
    Raises:
        RuntimeError: If the table cannot be updated due to an error.
    '''
    try:
        # Try to update table based on borough names to new population values
        with Session() as session:
            for boro_name, data in data_map.items():
                stmt = select(tableClass).where(tableClass.borough == boro_name)
                row = session.execute(stmt).scalar_one()
                row.population = data
                session.commit()
        return 0
    except Exception as e:
        raise RuntimeError(f'Could not update {tableClass}: {e}')


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')