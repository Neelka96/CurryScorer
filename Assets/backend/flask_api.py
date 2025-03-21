from sqlalchemy import func, select
from flask import Flask, jsonify, request, abort
from Assets.backend import flask_api as api
from Assets.etl import database as db
import datetime as dt

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Routes


# Endpoint for interactive heat map
@app.route('/api/v1.0/map')
def api_map():
    '''
    Returns restaurant markers with details for an interactive map.
    Each marker includes name, latitude, longitude, borough, cuisine, etc.
    '''
    with db.Session() as session:
        stmt = select(db.Restaurants)
        restaurants = session.scalars(stmt).all()
        data = [
            {
                'id': r.id,
                'name': r.name,
                'lat': r.lat,
                'lng': r.lng,
                'borough': r.borough.borough,
                'cuisine': r.cuisine.cuisine,
                'inspection_date': dt.date.isoformat(r.inspection_date)
            }
        for r in restaurants]
    return jsonify(data)



# @app.route('/api/v1.0/top-cuisines')
# def api_topCuisines():
#     '''
#     Returns aggregated counts for cuisines in a given borough.
#     Expects a borough query parameter, e.g., ?borough=Brooklyn.
#     '''
#     boro_param = request.args.get('borough')
#     with db.Session() as session:


if __name__ == '__main__':
    pass