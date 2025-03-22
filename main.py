from Assets import etl
from Assets.etl import database as db
from Assets.backend import flask_api as api
from Assets.etl import test

from pathlib import Path

if __name__ == '__main__':
    db_path = Path(db.engine.url.database)
    if db_path.exists():
        test.update_db()
    else:
        test.init_db()

    api.app.run(debug = True)