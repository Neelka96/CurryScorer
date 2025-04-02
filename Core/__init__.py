# Import dependencies
import pandas as pd
from pathlib import Path
from datetime import datetime as dt, timedelta as td

# Import Directory Modules for Core Building
from .etl import extract as E, transform as T, load as L
from .database import engine, Base, Boroughs, Cuisines, Restaurants

# Bring in custom logger
from .log_config import init_log


class Pipeline():
    def __init__(
            self
            ,db_config: dict[str, Path | str | td]
            ,api_config: dict[str, int | str]
            ,ref_seqs: dict[str, tuple]
            ,log_file: Path | str
            ):
        '''
        ETL Pipeline for managing the CurryScorer database.

        This class orchestrates the Extract, Transform, and Load (ETL) process
        for the CurryScorer project. It dynamically determines whether to perform
        a fresh ETL or update an existing database based on metadata.

        Attributes:
            db_config (dict): Configuration for the database engine and paths.
            api_config (dict): Configuration for API calls.
            ref_seqs (dict): Reference sequences for transformations.
            data (dict): Stores intermediate datasets during the ETL process.
        '''
        self.log = init_log(__name__, file = log_file)
        self.log.info('Initializing pipeline.')
        self.db_config = db_config
        self.api_config = api_config
        self.ref_seqs = ref_seqs
        self.data: dict[str, pd.DataFrame | dict] = {}
        self.metadata() # Call inital metadata setup to test for database attributes

    def metadata(self):
        self.log.info('Setting up metadata.')
        try:
            # Checks for existing database and logs it's timestamp if possible
            self.log.debug('Checking for existing database.')
            self.exists = True
            self.last_edit = dt.fromtimestamp(self.db_config['PATH'].stat().st_mtime)   # Last modified date
            self.log.debug('Database found!')
        except FileNotFoundError:  
            # If no database found, set attributes for initial setup scenario
            self.log.debug('No existing database found.')
            self.exists = False
            self.last_edit = dt.now()
        except Exception and not FileNotFoundError:
            # If there's an error outside accepted bounds raise
            self.log.critical('Could not instantiate metadata.', exc_info = True)
            raise
        finally:
            # Finally establish all 
            self.since_edit = dt.now() - self.last_edit  # Time since last update
            self.needs_update = True if self.since_edit > self.db_config['UPDATE_INTERVAL'] else False
            self.log.info('Metadata setup complete.')
        return self
    
    def extract(self):
        # Extracts data when needed, and checks for existing data when possible
        self.log.info('Extracting datasets...')
        self.data['dohmh'] = E.extraction('dohmh', self.api_config)
        self.data['fastfood'] = E.get_addData('fastfood', self.db_config['FASTFOOD_CSV'], self.api_config)
        self.data['population'] = pd.read_csv(self.db_config['POPULATION_CSV'])
        self.log.info('Extraction complete.')
        return self
    
    def transform(self, new_db: bool = True):
        # Bulked transformations broken down into helper functions for cleaning and normalization
        # Top level customization brough into pipeline for abstraction visibility
        self.log.info('Tranforming datasets...')
        borough_map = T.create_dict(self.ref_seqs['BOROUGHS'], lambda num: f'B{num}')
        cuisine_map = T.create_dict(self.ref_seqs['CUISINES'], lambda num: f'C{num}')
        fastfood_names = self.data['fastfood']['name'].to_list()
        main_df = T.clean_df(self.data['dohmh'], fastfood_names, cuisine_map.keys())
        main_df = T.normalize_table(main_df, borough_map, 'borough')
        self.data['restaurants'] = T.normalize_table(main_df, cuisine_map, 'cuisine')
        if new_db:
            # Full routine to be run for new databases
            self.log.warning('Full transformation subroutine selected. Creating reference tables.')
            self.data['boroughs'] = T.create_ref_table(borough_map, 'borough').merge(self.data['population'], how = 'left', on = 'borough')
            self.data['cuisines'] = T.create_ref_table(cuisine_map, 'cuisine')
        self.log.info('Tranformation complete.')
        return self

    def load(self, new_db: bool = True):
        # Checks if it's loading in a brand new database or not
        if new_db:
            self.log.info('Loading in new data...')
            Base.metadata.create_all(engine)    # Create tables with enforced schema, in proper order
            L.fresh_table(Boroughs, self.data['boroughs'])
            L.fresh_table(Cuisines, self.data['cuisines'])
            L.fresh_table(Restaurants, self.data['restaurants'])
        else:
            self.log.info('Updating existing data...')
            L.delete_expiredRows(Restaurants, self.api_config['DATE_CUTOFF'])
            L.update_restaurants(Restaurants, self.data['restaurants'])
            L.update_population(Boroughs, self.data['population'])
        self.log.info('Loading complete.')
        return self

    def run(self):
        # Runs according to boolean metadata determined during startup
        self.log.debug('Pipeline dynamic run started...')
        if not self.exists:
            self.log.debug('Attempting to do fresh ETL on database...')
            self.extract().transform().load()
        elif self.needs_update:
            self.log.debug('Attempting update on database...')
            self.extract().transform(new_db = False).load(new_db = False)
        self.log.info('Pipeline run complete.')
        return self


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')