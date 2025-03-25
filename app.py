import main
from Core.backend.database import engine
from Core import backend as api
import keys

# Import dependencies
from pathlib import Path

################################################
# Set API Keys for passing down to functions
nyc_open_key = keys.NYC_OPEN_KEY
# census_key = keys.CENSUS_KEY
################################################

# Collects Path of SQLite DataBase Engine if it exists
db_path = Path(engine.url.database)

# Run All DB Tests and Ops
main.run_db_ops(db_path, nyc_open_key)

# Serve up flask API
app = api.app


if __name__ == '__main__':
    api.app.run(debug = False, use_reloader = False)

# NOTE TO SELF:
# NEXT STEPS:
# 1. ADD METHOD FOR AUTO ETL OF POPULATION DATA
# 3. HOST LIVE BY CLASS!!!!!!!!!!!!!!!


# ADD ENDPOINT FOR FULL TABLE QUERYING WITHIN WEB BROWSER (MIGHT BE TOO DIFFICULT TO IMPLEMENT, CHECK IN LATER)


# Implement switch to header at some point if possible:
# headers = {
#     'X-App-Token': MY_APP_TOKEN_ID,
# }
# response = requests.get(api_url, headers=headers, params=other_params)


# CENSUS ETL TRACK

# Init db -> Call Census API -> ETL to df -> Save as CSV (for timestamp) -> Convert df to dictionary
# Updated db -> Check the date of the CSV file [Out of date] -> Call Census API -> ETL to df -> Save as CSV (for timestamp) -> Convert df to dictionary
#                                                  [In date] -> Don't do anything for populations


# Decouple population task from Main_Ops()
# Set up conditional within nested function to just be called by update db
# Allow init db to bypass and just call base functions to retrive data