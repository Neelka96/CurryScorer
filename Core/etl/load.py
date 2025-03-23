# Import dependencies
import pandas as pd
from sqlalchemy import Table, insert, delete
from sqlalchemy.orm import Session, sessionmaker


# Loading File

def freshTable(
        Session: sessionmaker[Session]
        ,tableClass: Table
        ,df: pd.DataFrame
        ) -> int:
    '''
    Deletes all existing data in the specified table and inserts new data from the provided DataFrame.

    Args:
        Session (sessionmaker[Session]): A session maker bound to an engine with configurations already, for accessing through the ORM Layer.
        tableClass (Table): The SQLAlchemy table class to create.
        df (pd.DataFrame): The DataFrame containing the new data to insert.

    Returns:
        int: Returns 0 upon successful completion.

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


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')