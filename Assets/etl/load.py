import pandas as pd
from sqlalchemy import Table, insert, delete
from . import database as db


def freshTable(TableClass: Table, df: pd.DataFrame) -> int:
    '''Starts from scratch, deletes existing data'''
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
    return freshTable(db.Boroughs, df)

def newCuisines(df: pd.DataFrame) -> int:
    return freshTable(db.Cuisines, df)

def newRestauants(df: pd.DataFrame) -> int:
    return freshTable(db.Restaurants, df)



if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')