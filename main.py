import extract as E
import transform as T
import database as db
import load as L

from sqlalchemy.ext.automap import automap_base
from flask import Flask, jsonify, request, abort


#     # Build drop lists
#     if not csvPath.exists() or force_download:
#         drop_names = Extraction('fast_food')['name'].unique()
#         pd.Series({'name': drop_names}).to_csv(csvPath, header = True, index = False)

#     drop_names = pd.read_csv(csvPath)

if __name__ == '__main__':
    print('Not scripted yet.')