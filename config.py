# Import dependencies
import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# Bring in custom logger
from Core.log_config import init_log
log = init_log(__name__)


# GRABBING ENV VARIABLES
load_dotenv()
ENV = os.environ.get('ENV', 'development')  # Retrieved ENV value for dev/production
log.debug(f'Environment variables loaded in. Current env is {ENV}.')

# Non Variable Paths
CORE_DIR = Path(__file__).resolve().parent / 'Core'
TEMPLATE_DIR = CORE_DIR / 'backend' / 'templates'   # Flask Templates Directory for HTML Rendering 


# Variable Paths - Random comment for test
DEF_STORAGE = '/mount/shared'
if ENV == 'production':
    STORAGE = Path(os.environ.get('STORAGE', DEF_STORAGE))
    DB_PATH = STORAGE / 'courier.sqlite'
else:
    STORAGE = CORE_DIR / 'resources'
    DB_PATH = STORAGE / 'courier_dev.sqlite'
log.info(f'(Storage, DataBase) Paths => ({STORAGE}, {DB_PATH})')

if ENV == 'production' and STORAGE != Path(DEF_STORAGE):
    log.warning(f'Production storage path is incorrect: {STORAGE}')


# Paths for Persistent Storage Locally & Live
DB_CONFIG = {
    'PATH': DB_PATH
    ,'ENGINE_URI': f'sqlite:///{DB_PATH}'
    ,'UPDATE_INTERVAL': timedelta(weeks = 2)
    ,'FASTFOOD_CSV': STORAGE / 'fastfood.csv'
    ,'POPULATION_CSV': STORAGE / 'census_population.csv'
}

# NYC Open API Configuration
API_CONFIG = {
    'KEY': os.environ.get('NYC_OPEN_KEY')   # Retrieve NYC Open Key
    ,'ROW_LIMIT': 200000     # Max limit for rows returned by API
    ,'DATE_CUTOFF': 2   # In years, describes max years allowed since last inspection.
    ,'TIMEOUT': 15  # In seconds, requests.get() request timeout cutoff.
    ,'RETRY': 2     # Number of retries for API calls - used in core get_df() function.
    ,'DELAY': 10    # In seconds, delay upon retry before another request is sent out.
    ,'SLEEP': 10    # In seconds, sleep time between two different API calls for a similar website - only needed during init db construction.
}


# Transformation Constants
REF_SEQS = {
    'BOROUGHS': (
        'Manhattan', 'Bronx', 'Brooklyn', 'Queens', 'Staten Island'
    )
    ,'CUISINES': (
        'Afghan'
        ,'African'
        ,'Armenian'
        ,'Australian'
        ,'Bangladeshi'
        ,'Basque'
        ,'Brazilian'
        ,'Cajun'
        ,'Californian'
        ,'Caribbean'
        ,'Chilean'
        ,'Chinese'
        ,'Chinese/Japanese'
        ,'Creole'
        ,'Creole/Cajun'
        ,'Czech'
        ,'Eastern European'
        ,'Egyptian'
        ,'English'
        ,'Ethiopian'
        ,'Filipino'
        ,'French'
        ,'German'
        ,'Greek'
        ,'Haute Cuisine'
        ,'Hawaiian'
        ,'Indian'
        ,'Indonesian'
        ,'Iranian'
        ,'Irish'
        ,'Italian'
        ,'Japanese'
        ,'Jewish/Kosher'
        ,'Korean'
        ,'Latin American'
        ,'Lebanese'
        ,'Mediterranean'
        ,'Mexican'
        ,'Middle Eastern'
        ,'Moroccan'
        ,'New French'
        ,'Pakistani'
        ,'Peruvian'
        ,'Polish'
        ,'Portuguese'
        ,'Russian'
        ,'Scandinavian'
        ,'Soul Food'
        ,'Southeast Asian'
        ,'Spanish'
        ,'Tapas'
        ,'Thai'
        ,'Turkish'
    )
}


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')