# Configuration File

# Import dependencies
import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

################################################################################################################################################
# VERY IMPORTANT: UPDATE INTERVAL, PLEASE SPECIFY AS TIMEDELTA OBJECT
# (If you're not familiar with timedelta objects, hover over the class for a hint, or put a comma after the `2` in `weeks = 2` for more info)
UPDATE_INTERVAL = timedelta(weeks = 2)
################################################################################################################################################

################################################################################################################################################
# GRABBING ENV VARIABLES
load_dotenv()
NYC_OPEN_KEY = os.environ.get('NYC_OPEN_KEY')   # Retrieve NYC Open Key
CENSUS_KEY = os.environ.get('CENSUS_KEY')   # Retrieves Census Key
ENV = os.environ.get('ENV', 'development')  # Retrieved ENV value for dev/production
################################################################################################################################################

# Non Variable Paths
CORE_DIR = Path(__file__).resolve().parent / 'Core'
TEMPLATE_DIR = CORE_DIR / 'backend' / 'templates'   # Flask Templates Directory for HTML Rendering 

# Variable Paths
if ENV == 'production':
    STORAGE = Path('/home/site/shared')
    DB_PATH = STORAGE / 'courier.sqlite'
else:
    STORAGE = CORE_DIR / 'resources'
    DB_PATH = STORAGE / 'courier_dev.sqlite'

# Persistent Storage in both environments
FASTFOOD_CSV = STORAGE / 'fastfood.csv'
POPULATION_CLEAN = STORAGE / 'census_population.csv'
ENGINE_URI = f'sqlite:///{DB_PATH}' # Full engine path to avoid hardcoding later


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