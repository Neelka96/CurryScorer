# Import modules for core controlling from here

# import Core
from Core import test
from Core.backend.database import engine
from Core import backend as api

# Import dependencies
from pathlib import Path


if __name__ == '__main__':
    '''
    Main entry point for the application. Initializes or updates the database
    and starts the Flask API server.
    '''
    db_path = Path(engine.url.database)
    if db_path.exists():
        test.update_db()
    else:
        test.init_db()

    api.app.run(debug = True)


# NOTE TO SELF:
# NEXT STEPS:
# 1. ADD METHOD FOR AUTO ETL OF POPULATION DATA
# 2. ADD ENDPOINT FOR FULL TABLE QUERYING WITHIN WEB BROWSER
#   - Add proper html styling for home node
# 3. TEST FOR ALL ANGLES
# 6. Requests needs headers for API/APP Key