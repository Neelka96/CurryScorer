# Import Dependencies
from sqlalchemy import create_engine, event, Engine, ForeignKey, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

import config as C

# SQLITE BACKEND ARCHITECTURE

# Create ORM base var
Base = declarative_base()


# Secondary ref table for boroughs
class Boroughs(Base):
    '''
    Represents the boroughs table in the database.

    Attributes:
        borough_id (String): The primary key, representing the unique ID of the borough.
        borough (String): The name of the borough.
        population (int): The population of the borough.
    '''
    # Table name
    __tablename__ = 'boroughs'

    # Columns
    borough_id = Column(String, primary_key = True)
    borough = Column(String, nullable = False)
    population = Column(Integer, nullable = True)


# Secondary ref table for cuisines
class Cuisines(Base):
    '''
    Represents the cuisines table in the database.

    Attributes:
        cuisine_id (String): The primary key, representing the unique ID of the cuisine.
        cuisine (String): The name of the cuisine.
    '''
    # Table name
    __tablename__ = 'cuisines'

    # Columns
    cuisine_id = Column(String, primary_key = True)
    cuisine = Column(String, nullable = False)


# Main Table (Restaurant)
class Restaurants(Base):
    '''
    Represents the restaurants table in the database.

    Attributes:
        id (Integer): The primary key, representing the unique ID of the restaurant.
        name (String): The name of the restaurant.
        borough_id (String): Foreign key referencing the boroughs table.
        cuisine_id (String): Foreign key referencing the cuisines table.
        inspection_date (DateTime): The date of the last inspection.
        lat (Float): The latitude of the restaurant's location.
        lng (Float): The longitude of the restaurant's location.

    Relationships:
        borough (Boroughs): Relationship to the Boroughs table.
        cuisine (Cuisines): Relationship to the Cuisines table.
    '''
    # Table name
    __tablename__ = 'restaurants'

    # Columns
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    borough_id = Column(String, ForeignKey('boroughs.borough_id'), nullable = False)
    cuisine_id = Column(String, ForeignKey('cuisines.cuisine_id'), nullable = False)
    inspection_date = \
        Column(DateTime, nullable = False)
    lat = Column(Float, nullable = False)
    lng = Column(Float, nullable = False)

    # Relationships with reference tables, accessable through gateway now
    borough = relationship('Boroughs', backref = 'restaurants')
    cuisine = relationship('Cuisines', backref = 'restaurants')

    # What is shown when print or string is called on object
    def __repr__(self):
        '''
        Creates string definition for Restaurant object.

        Returns:
            str: String representation of the restaurant.
        '''
        f'<RestaurantTable(id={self.id}, name="{self.name}")>'


# Create IMPORTANT ENGINE to be used across namespaces
engine = create_engine(C.SQLALCHEMY_URI)

# Event listener for engine connection, enforces foreign keys upon connection
@event.listens_for(Engine, 'connect')
def enforce_sqlite_fks(dbapi, conn_record):
    '''
    Enforces foreign key constraints in SQLite.

    Args:
        dbapi: The database API.
        conn_record: The connection record.
    '''
    cursor = dbapi.cursor()
    cursor.execute('PRAGMA foreign_keys=ON;')
    cursor.close()

# Bind session to engine now that modifications to engine are done
Session = sessionmaker(bind = engine)



if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')