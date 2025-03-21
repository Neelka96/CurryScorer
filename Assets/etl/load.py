import pandas as pd
from sqlalchemy import Table, insert, select, delete
from . import database as db

# , inspect, create_engine, event, Engine, ForeignKey, Column, Integer, Float, String, DateTime
# from sqlalchemy.orm import sessionmaker, declarative_base, relationship
# from sqlalchemy.ext.automap import automap_base

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

def getTable(TableClass: Table) -> pd.DataFrame:
    TableClass
    with db.Session() as session:
        result = session.execute(select(TableClass)).all()
        session.flush()
    return pd.DataFrame(result)

# Set Wrappers for access and writing using df

def newRestauants(df: pd.DataFrame) -> int:
    return freshTable(db.Restaurants, df)

def newBoroughs(df: pd.DataFrame) -> int:
    return freshTable(db.Boroughs, df)

def newCuisines(df: pd.DataFrame) -> int:
    return freshTable(db.Cuisines, df)


def getRestaurants() -> pd.DataFrame:
    return getTable(db.Restaurants)

def getBoroughs() -> pd.DataFrame:
    return getTable(db.Boroughs)

def getCuisines() -> pd.DataFrame:
    return getTable(db.Cuisines)