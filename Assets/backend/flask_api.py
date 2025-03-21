from sqlalchemy import func, select
from flask import Flask, jsonify, request, abort
from Assets.backend import flask_api as api
from Assets.etl import database as db

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Routes


@app.route('/api/v1.0/map')
def interactive_map():
    '''
    Returns restaurant markers with details for an interactive map.
    Each marker includes name, latitude, longitude, borough, cuisine, etc.
    '''
    with db.Session() as session:
        stmt = select(db.Restaurants)
        restaurants = session.scalar(stmt).all()
    data = [
        {
            'id': r.id,
            'name': r.name,
            'lat': r.lat,
            'lng': r.lng,
            'borough': r.borough.borough,
            'cuisine': r.cuisine.cuisine,
            'inspection_date': r.inspection_date.fromisoformat()
        }
        for r in restaurants]
    return jsonify(data)


if __name__ == '__main__':
    pass