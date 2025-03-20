# Import Dependencies
from sqlalchemy import create_engine, event, Engine, ForeignKey, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
# from sqlalchemy.ext.automap import automap_base


# SQLITE BACKEND ARCHITECTURE

# Create ORM base var
Base = declarative_base()

# Secondary ref table for boroughs
class Boroughs(Base):
    __tablename__ = 'boroughs'

    borough_id = Column(String, primary_key = True)
    borough = Column(String, nullable = False)
    # population = Column(int, nullable = False)

# Secondary ref table for cuisines
class Cuisines(Base):
    __tablename__ = 'cuisines'

    cuisine_id = Column(String, primary_key = True)
    cuisine = Column(String, nullable = False)

# Main Table (Restaurant)
class Restaurants(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False, unique = True)
    borough_id = Column(String, ForeignKey('boroughs.borough_id'), nullable = False)
    cuisine_id = Column(String, ForeignKey('cuisines.cuisine_id'), nullable = False)
    inspection_date = \
        Column(DateTime, nullable = False)
    lat = Column(Float, nullable = False)
    lng = Column(Float, nullable = False)

    borough = relationship('boroughs', backref = 'restaurants')
    cuisine = relationship('cuisines', backref = 'restaurants')

    def __repr__(self):
        f'<RestaurantTable(id={self.id}, name="{self.name}")>'


# Create engine, bind sessions to it, and create tables
engine = create_engine('sqlite:///courier.sqlite')

@event.listens_for(Engine, 'connect')
def enforce_sqlite_fks(dbapi, conn_record):
    cursor = dbapi.cursor()
    cursor.execute('PRAGMA foreign_keys=ON;')
    cursor.close()

Session = sessionmaker(bind = engine)

if __name__ == '__main__':
    pass