# Import dependencies
from sqlalchemy import func, select
from flask import Flask, jsonify, request, abort
import datetime as dt

# Import subpackage dependencies
from Assets.etl.database import Restaurants, Boroughs, Cuisines, Session
from . import backend as api

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Endpoint Declarations
heat_map_node = '/api/v1.0/map'
top_cuisines_node = '/api/v1.0/top-cuisines/'
cuisine_dist_node = '/api/v1.0/cuisine-distribution'


#################################################
# Flask Endpoints
#################################################

# Endpoint for home
@app.route('/')
def home():
    return api.home_html


# Endpoint for interactive heat map
@app.route(heat_map_node)
def api_map():
    '''
    Returns restaurant markers with details for an interactive map.
    Each marker includes name, latitude, longitude, borough, cuisine, etc.
    '''
    with Session() as session:
        stmt = select(Restaurants)
        results = session.scalars(stmt).all()
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
        for r in results]
    desc = 'Retrieves restaurant details for interactive heat map.'
    data_nest = api.format_json(heat_map_node, data, desc)
    return jsonify(data_nest)


# Endpoint for bar chart
@app.route(top_cuisines_node)
def api_topCuisines():
    '''
    Returns aggregated counts for cuisines in a given borough.
    Expects a borough query parameter, e.g., ?borough=Brooklyn.
    '''
    boro_param = request.args.get('borough')
    with Session() as session:
        count_ids = func.count(Restaurants.id)
        stmt = (
            select(
                Cuisines.cuisine.label('cuisine')
                ,count_ids.label('count')
            ).join(
                Restaurants
                ,Restaurants.cuisine_id == Cuisines.cuisine_id
            ).join(
                Boroughs
                ,Boroughs.borough_id == Restaurants.borough_id
            ).where(
                Boroughs.borough == boro_param
            ).group_by(
                Cuisines.cuisine
            ).order_by(
                count_ids.desc()
            )
        )
        results = session.execute(stmt).all()
        data = [
            {
                'cuisine': r.cuisine,
                'count': r.count
            } 
        for r in results]
    desc = 'Retrieves aggregated counts for cuisines in given borough.'
    params = {'borough': boro_param}
    data_nest = api.format_json(top_cuisines_node, data, desc, params)
    return jsonify(data_nest)


# Endpoint for total pie chart
@app.route(cuisine_dist_node)
def api_cuisine_pie():
    '''
    Returns the percentage distribution of different ethnic cuisines across the city.
    '''
    with Session() as session:
        stmt_total = select(func.count(Restaurants.id))
        total = session.scalars(stmt_total)

        stmt = (
            select(
                Cuisines.cuisine.label('cuisine')
                ,func.count(Restaurants.id).label('count')
            ).join(
                Restaurants
                ,Restaurants.cuisine_id == Cuisines.cuisine_id
            ).group_by(Cuisines.cuisine)
        )

        results = session.execute(stmt).all()
        data = [
            {
                'cuisine': r.cuisine
                ,'count': r.count
                ,'percent': (r.count / total * 100)
            }
        for r in results]
    desc = 'Retrieves percent distribution of all cuisines across NYC.'
    data_nest = api.format_json(cuisine_dist_node, data, desc)
    return jsonify(data_nest)



if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')