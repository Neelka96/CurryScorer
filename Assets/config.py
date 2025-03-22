# Configuration File

# Import dependencies
from pathlib import Path


# Paths
ASSETS_DIR = Path(__file__).resolve().parent    # Base Assets Directory
CLEAN_DATA_DIR = ASSETS_DIR / 'data' / 'clean'  # Assets/data/clean directory
FASTFOOD_CSV = CLEAN_DATA_DIR / 'fastfood.csv'  # clean/fastfood.csv
CENSUS_CSV = CLEAN_DATA_DIR / 'NYC_Boroughs_Data.csv'   # clean/NYC_Boroughs_Data.csv


# PATHS FOR TESTING PURPOSES
DOHMH_CLEAN = CLEAN_DATA_DIR / 'dohmh_clean.csv' # clean/dohmh_clean.csv


# Filter Constants
ROW_LIMIT = 200000  # Max limit for rows returned by API
INSPECTION_CUTOFF = 2   # In years, describes max years allowed since last inspection.


# API Constants
SLEEP_TIME = 5  # In seconds, sleep time between two different API calls for a similar website - only needed during init db construction.
API_TIMEOUT = 15    # In seconds, requests.get() request timeout cutoff.
API_RETRY = 2   # Number of retries for API calls - used in core get_df() function.
API_DELAY = 10  # In seconds, delay upon retry before another request is sent out.


# Transformation Constants
BOROUGHS = (
    'Manhattan', 'Bronx', 'Brooklyn', 'Queens', 'Staten Island'
)
CUISINES = (
    'Afghan',
    'African',
    'American',
    'Armenian',
    'Australian',
    'Bangladeshi',
    'Basque',
    'Brazilian',
    'Cajun',
    'Californian',
    'Caribbean',
    'Chilean',
    'Chinese',
    'Chinese/Japanese',
    'Creole',
    'Creole/Cajun',
    'Czech',
    'Eastern European',
    'Egyptian',
    'English',
    'Ethiopian',
    'Filipino',
    'French',
    'German',
    'Greek',
    'Haute Cuisine',
    'Hawaiian',
    'Indian',
    'Indonesian',
    'Iranian',
    'Irish',
    'Italian',
    'Japanese',
    'Jewish/Kosher',
    'Korean',
    'Latin American',
    'Lebanese',
    'Mediterranean',
    'Mexican',
    'Middle Eastern',
    'Moroccan',
    'New French',
    'Pakistani',
    'Peruvian',
    'Polish',
    'Portuguese',
    'Russian',
    'Scandinavian',
    'Soul Food',
    'Southeast Asian',
    'Spanish',
    'Tapas',
    'Thai',
    'Turkish'
)


if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')