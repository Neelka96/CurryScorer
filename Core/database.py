# Import Dependencies
from contextlib import contextmanager
from datetime import datetime as dt
from collections.abc import Sequence, Generator
from sqlalchemy import create_engine, event, Engine, ForeignKey, String, Numeric, Select, Row
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column, relationship, Session as SessionType
from sqlalchemy.sql import Executable

# Import configuration
import config as C

# Bring in custom logger
from Core.log_config import init_log
log = init_log(__name__)


# Create ORM base class
class Base(DeclarativeBase):
    pass


# Secondary ref table for boroughs
class Boroughs(Base):
    '''
    Represents the boroughs parent table in the database.

    Attributes:
        borough_id (String): PK representing the unique ID.
        borough (String): The boroughs's name.
        population (int): The boroughs's population.
    '''
    # Table name
    __tablename__ = 'boroughs'

    # Columns
    borough_id: Mapped[str] = mapped_column(String(2), primary_key = True)
    borough: Mapped[str] = mapped_column(nullable = False)
    population: Mapped[int] = mapped_column(nullable = True)

    # Relationships
    restaurants: Mapped[list['Restaurants']] = relationship(back_populates = 'borough')

    def __repr__(self):
        return f'<BoroughTable(id={self.borough_id}, borough={self.borough})>'



# Secondary ref table for cuisines
class Cuisines(Base):
    '''
    Represents the cuisines parent table in the database.

    Attributes:
        cuisine_id (String): PK representing the unique ID.
        cuisine (String): The name of the cuisine.
    '''
    # Table name
    __tablename__ = 'cuisines'

    # Columns
    cuisine_id: Mapped[str] = mapped_column(primary_key = True)
    cuisine: Mapped[str] = mapped_column(nullable = False)

    # Relationships
    restaurants: Mapped[list['Restaurants']] = relationship(back_populates = 'cuisine')

    def __repr__(self):
        return f'<CuisineTable(id={self.cuisine_id}, cuisine={self.cuisine})>'



# Main Table (Restaurant)
class Restaurants(Base):
    '''
    Represents the restaurants table in the database.

    Attributes:
        id (Integer): PK representing the unique ID of the location.
        name (String): The name of the location.
        borough_id (String): FK reference to Boroughs table.
        cuisine_id (String): FK reference to Cuisines table.
        inspection_date (DateTime): The date of the last inspection.
        lat (Float): The location's latitude.
        lng (Float): The location's longitude.

    Relationships:
        borough (Boroughs): Many-to-one relation to Boroughs table.
        cuisine (Cuisines): Many-to-one relation to Cuisines table.
    '''
    # Table name
    __tablename__ = 'restaurants'

    # Columns
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(nullable = False)
    borough_id: Mapped[str] = mapped_column(String(2), ForeignKey('boroughs.borough_id'), nullable = False)
    cuisine_id: Mapped[str] = mapped_column(ForeignKey('cuisines.cuisine_id'), nullable = False)
    inspection_date: Mapped[dt] = mapped_column(nullable = False)
    lat: Mapped[float] = mapped_column(Numeric(14, 12), nullable = False)
    lng: Mapped[float] = mapped_column(Numeric(14, 12), nullable = False)

    # Relationships with reference tables, accessable through gateway now
    borough: Mapped['Boroughs'] = relationship(back_populates = 'restaurants')
    cuisine: Mapped['Cuisines'] = relationship(back_populates = 'restaurants')

    # What is shown when print or string is called on object
    def __repr__(self):
        return f'<RestaurantTable(id={self.id}, name="{self.name}")>'


# Create IMPORTANT ENGINE to be used across namespaces
engine = create_engine(C.DB_CONFIG['ENGINE_URI'])

# Event listener for engine connection, enforces foreign keys upon connection
@event.listens_for(Engine, 'connect')
def enforce_sqlite_fks(dbapi, conn_record):
    cursor = dbapi.cursor()
    cursor.execute('PRAGMA foreign_keys=ON;')
    cursor.close()
    return 0

# Bind session to engine now that modifications to engine are done
Session = sessionmaker(bind = engine, expire_on_commit = False)


# Context management handler for sessions for centralized handling
@contextmanager
def get_session() -> Generator[SessionType]:
    '''Custom session context manager for SQL Alchemy.

    Yields:
        Generator[SessionType]: New session from bound engine connection pool.
    '''
    session = Session()
    try:
        yield session
        session.commit()
        log.debug('Session successfully committed.')
    except Exception:
        session.rollback()
        log.critical('Session rollback from error.')
        raise 
    finally:
        session.close()
        log.debug('Closing session.')


# Utility For executing session requests
def execute_query(
        stmt: Executable
        ,params: dict | Sequence[dict] | None = None
        ) -> Sequence[Row] | int:
    '''Wrapper for custom context manager for simple and bulk queries.

    Args:
        stmt (Executable): `Select`, `Insert`, `Delete`, and other Core `SQL` clause types.
        params (dict | Sequence[dict] | None, optional): Data or constraints to be used. Defaults to None.

    Returns:
        Sequence[Row]: Returns view of data from `Select` type.
        int: Non-select executable type returns 0.
    '''
    with get_session() as session:
        log.debug('execute_query() called.')
        try:
            result = session.execute(stmt, params) if params else session.execute(stmt)
            log.debug('execute_query() successfully utilized.')
            return result.scalars().all() if isinstance(stmt, Select) else 0 # For success
        except Exception:
            log.critical('Could not use BP reduced execute_query() function.')
            raise


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')