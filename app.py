import main
from Core.backend.database import engine
from Core.backend import app
import config as C


# Run with app_context to try to execute on top of app declaration
# if that doesn't work than move to blueprinting Flask or creating it modularly down stream
with app.app_context():
    # Run All DB Tests and Ops
    main.run_db_ops(C.DB_PATH, C.NYC_OPEN_KEY)

# Serve up flask API
app


if __name__ == '__main__':
    # Run All DB Tests and Ops
    main.run_db_ops(C.DB_PATH, C.NYC_OPEN_KEY)

    # Serve up flask API
    app.run(debug = False, use_reloader = False)