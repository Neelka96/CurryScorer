# Import modules for core controlling from here
import Core
import config as C

# Import dependencies
from pathlib import Path
from datetime import datetime as dt


def run_db_ops(db_path: Path, nyc_open_key: str) -> int:
    '''
    Main entry point for the application. Initializes or updates the database depending on the current date and time, and the time since your last update.
    '''
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
    
    return 0