from Core import backend as api

app = api.app

if __name__ == '__main__':
    '''
    Main entry point for the application. Initializes or updates the database depending on the current date and time, and the time since your last update.
    Afterwards, it will always serve up Flask API for fetching.
    '''
    # Import modules for core controlling from here
    import Core
    from Core.backend.database import engine
    from Core import backend as api
    import config as C
    import keys

    # Import dependencies
    from pathlib import Path
    from datetime import datetime as dt

    ################################################
    # Set API Keys for passing down to functions
    nyc_open_key = keys.NYC_OPEN_KEY
    census_key = keys.CENSUS_KEY
    ################################################

    # Collects Path of SQLite DataBase Engine if it exists
    db_path = Path(engine.url.database)

    # Tries to collect timestamp from engine, if it doesn't exist create the database
    try:
        # Last modified date
        last_modified = dt.fromtimestamp(db_path.stat().st_mtime)
        
        # Calculated time since last update
        since_last_update = dt.now() - last_modified

        # If the last update time exceeds the time set in your config.py file found in the route, your database will update
        if since_last_update > C.UPDATE_INTERVAL:
            print(f'Wow, it\'s been {since_last_update} since your last update! Time for an update.')
            try:
                print('Updating DataBase (Restaurant Table and Population in Boroughs)...')
                Core.update_db(nyc_open_key)
                print(
                    'Success!\n'
                    'Serving up API...'
                )
            except Exception as e:
                raise e
            
        # If it's not out-of-date, your database will simply be used to serve up the API
        else:
            print('Your database is up-to-date! Serving up API...\n')

    # If the file isn't found, database creation is started
    except FileNotFoundError as e:
        print('DataBase not found, initializing...')
        Core.init_db(nyc_open_key)
        print('DataBase successfully created! Serving up API...\n')

    # Serve up flask API
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