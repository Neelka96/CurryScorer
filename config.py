# Configuration File

# Import dependencies
from pathlib import Path
from datetime import timedelta

################################################################################################################################################
# VERY IMPORTANT: UPDATE INTERVAL, PLEASE SPECIFY AS TIMEDELTA OBJECT
# (If you're not familiar with timedelta objects, hover over the class for a hint, or put a comma after the `2` in `weeks = 2` for more info)
UPDATE_INTERVAL = timedelta(weeks = 2)
################################################################################################################################################

# Paths
PERS_STORAGE = Path('/home')
CORE_DIR = PERS_STORAGE / 'Core' # Main Core Directory
DATA_DIR = CORE_DIR / 'data'    # Core/data
FASTFOOD_CSV = DATA_DIR / 'fastfood.csv'    # CSV PATH: data/fastfood.csv
POPULATION_CLEAN = DATA_DIR / 'census_population.csv'   # CSV PATH: data/census_population.csv
TEMPLATE_DIR = CORE_DIR / 'backend' / 'templates'   # Flask Templates Directory for HTML Rendering 

DB_PATH = PERS_STORAGE / 'courier.sqlite'
SQLALCHEMY_URI = f'sqlite:///{DB_PATH}'

# Filter Constants
ROW_LIMIT = 200000  # Max limit for rows returned by API
INSPECTION_CUTOFF = 2   # In years, describes max years allowed since last inspection.


# API Constants
SLEEP_TIME = 10  # In seconds, sleep time between two different API calls for a similar website - only needed during init db construction.
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