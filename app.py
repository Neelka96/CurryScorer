import main
from Core.backend.database import engine
from Core.backend import app
import config as C

# Import dependencies
from pathlib import Path

# Add last decorator to include ETL and DB Creation/Updating
@app.before_first_request
def init():
    # Run All DB Tests and Ops
    main.run_db_ops(C.DB_PATH, C.NYC_OPEN_KEY)

# Serve up flask API
app


if __name__ == '__main__':
    # Collects Path of SQLite DataBase Engine if it exists
    db_path = Path(engine.url.database)

    # Run All DB Tests and Ops
    main.run_db_ops(db_path, C.NYC_OPEN_KEY)

    # Serve up flask API
    app.run(debug = False, use_reloader = False)