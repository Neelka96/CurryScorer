# Import dependencies
import pandas as pd
from sqlalchemy import select, insert
from sqlalchemy.orm import DeclarativeMeta
from datetime import datetime as dt, timedelta as td

# Import subpackage dependencies
from Core.database import Boroughs, Restaurants, get_session, execute_query

# Bring in custom logger
from Core.log_config import init_log
log = init_log(__name__)


def fresh_table(
        tableClass: DeclarativeMeta
        ,df: pd.DataFrame
        ) -> int:
    '''Creates new table, expects blank table.

    Args:
        tableClass (DeclarativeMeta): Staged table.
        df (pd.DataFrame): Data to write to table.

    Returns:
        int: Rows changed.
    '''
    log.debug('Building fresh table.')
    try:    # Try to delete the table and insert it from scratch
        stmt = insert(tableClass)
        vals = df.to_dict('records')
        execute_query(stmt, vals) # Combining of insert() from core w/ session.execute() utilizes ORM layer
        log.debug('Table built successfully.')
        return f'{len(vals)} rows added.'
    except Exception:
        log.critical('Could not build fresh table.', exc_info = True)
        raise


def delete_expiredRows(
        tableClass: type[Restaurants]
        ,cutoff_years: int
        ) -> int:
    '''Deletes expired rows from child table.

    Args:
        tableClass (type[Restaurants]): Staged table.
        cutoff_years (int): Max number of years before cutoff.

    Returns:
        int: Rows changed.
    '''
    log.debug('Deleting expired rows.')
    cutoff_date = dt.now() - td(days = cutoff_years * 365)
    try:
        with get_session() as session:
            stmt = select(tableClass).where(tableClass.inspection_date < cutoff_date)
            restaurants = session.scalars(stmt).all()
            [session.delete(r) for r in restaurants]
        log.debug('Rows deleted successfully.')
        return f'{len(restaurants)} rows deleted.'
    except Exception:
        log.critical('Could not delete expired rows.', exc_info = True)
        raise


def update_restaurants(
        tableClass: type[Restaurants]
        ,data_df: pd.DataFrame
        ) -> int:
    '''Updated rows from child table.

    Args:
        tableClass (type[Restaurants]): Staged table.
        data_df (pd.DataFrame): Data for writing to table.

    Returns:
        int: Rows changed.
    '''
    log.debug('Updating rows.')
    try:
        with get_session() as session:
            rows_affected = 0
            for _, row in data_df.iterrows():
                stmt = select(tableClass).where(tableClass.id == row['id'])
                existing_row = session.execute(stmt).scalar_one_or_none()
                if existing_row is None:
                    session.add(tableClass(**row.to_dict())) 
                    rows_affected += 1
        log.debug('Rows updated successfully.')
        return f'{rows_affected} rows updated.'
    except Exception:
        log.critical('Could not update rows.', exc_info = True)
        raise


def update_population(
        tableClass: type[Boroughs]
        ,data_df: pd.DataFrame
        ) -> int:
    '''Updates rows from parents table.

    Args:
        tableClass (type[Boroughs]): Staged table.
        data_df (pd.DataFrame): Data for writing to table.

    Returns:
        int: Rows changed.
    '''
    log.debug('Updating rows.')
    try:    # Try to update table based on borough names to new population values
        with get_session() as session:
            rows_affected = 0
            for _, r in data_df.iterrows():
                stmt = select(tableClass).where(tableClass.borough == r['borough'])
                result = session.execute(stmt).scalar_one_or_none()
                if result:
                    result.population = r['population']
                    rows_affected += 1
        log.debug('Rows updated successfully.')
        return f'{rows_affected} rows updated.'
    except Exception:
        log.critical('Could not update rows.', exc_info = True)
        raise


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')