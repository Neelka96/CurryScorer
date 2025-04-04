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
log.info(f'Environment variables loaded. ENV is {ENV}.')

# Non Variable Paths
CORE_DIR = Path(__file__).resolve().parent / 'Core'
TEMPLATE_DIR = CORE_DIR / 'backend' / 'templates'   # Flask Templates Directory for HTML Rendering 


# Variable Paths
DEF_STORAGE = Path('/mnt/shared')
if ENV == 'production':
    STORAGE = DEF_STORAGE
    DB_PATH = STORAGE / 'courier.sqlite'
elif ENV == 'development':
    STORAGE = CORE_DIR / 'resources'
    DB_PATH = STORAGE / 'courier_dev.sqlite'
elif ENV is None:
    log.critical('No ENV environment variable has been declared. Be advised - emergency routes being used.')
    STORAGE = CORE_DIR / 'resources'
    DB_PATH = STORAGE / 'courier_dev.sqlite'

if ENV == 'production' and STORAGE != DEF_STORAGE:
    log.critical(f'Production storage path is incorrect: {STORAGE}')

# Logs Storage & DataBase Paths for environment integrity
log.info(f'Storage: {STORAGE}') if len(STORAGE.parts) <= 2 else log.info(f'Storage: .../{STORAGE.parts[-2]}/{STORAGE.parts[-1]}')
log.info(f'DataBase: {DB_PATH.name}')


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