import main
from Core.backend.database import engine
from Core.backend import app
import config as C

# Import dependencies
from pathlib import Path


if __name__ == '__main__':
    # Collects Path of SQLite DataBase Engine if it exists
    db_path = Path(engine.url.database)

    # Run All DB Tests and Ops
    main.run_db_ops(db_path, C.NYC_OPEN_KEY)

    # Serve up flask API
    app.run()


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