from Assets import etl
from Assets.etl import database as db
from Assets.backend import flask_api as api

from pathlib import Path

if __name__ == '__main__':
    # db_path = Path(db.engine.url.database)
    # links = {
    #     'cuisine': Path('Assets/data/cuisine_bins/keep.txt')
    #     ,'fast_food': Path('Assets/data/clean/fastfood.csv')
    # }
    # if db_path.exists():
    #     etl.update_db(links)
    # else:
    #     etl.init_db(links)

    db_path = Path(db.engine.url.database)
    links = {
        'cuisine': Path('Assets/data/cuisine_bins/keep.txt')
        ,'fast_food': Path('Assets/data/clean/fastfood.csv')
    }
    if db_path.exists():
        etl.testing_update(links, Path('Assets/data/clean/dohmh_clean.csv'))
    else:
        etl.testing_create(links, Path('Assets/data/clean/dohmh_clean.csv'))

    api.app.run(debug = True)