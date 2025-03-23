# Import modules for core controlling from here

# from Assets import etl
from Assets.etl import test
from Assets.backend import database as db
from Assets import backend as api

# Import dependencies
from pathlib import Path

if __name__ == '__main__':
    '''
    Main entry point for the application. Initializes or updates the database
    and starts the Flask API server.
    '''
    db_path = Path(db.engine.url.database)
    if db_path.exists():
        test.update_db()
    else:
        test.init_db()

    api.app.run(debug = True)