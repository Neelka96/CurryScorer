# Import dependencies
from sqlalchemy import func, select
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
import datetime as dt

# Import subpackage dependencies
from .backend import execute_query, forge_json
from .database import Restaurants, Boroughs, Cuisines
import config as C

#################################################
# Flask Setup
#################################################
app = Flask(__name__, template_folder = C.TEMPLATE_DIR)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto = 1, x_host = 1)
CORS(app)
app.json.sort_keys = False
app.url_map.strict_slashes = False

# Endpoint Declarations
map_node = '/api/v1.0/map/'
topCuisines_node = '/api/v1.0/top-cuisines/'
cuisineDist_node = '/api/v1.0/cuisine-distributions/'
boroughSummary_node = '/api/v1.0/borough-summaries/'


#################################################
# Flask Endpoints
#################################################

# Endpoint for home
@app.route('/')
def home():
    '''
    Home endpoint for the API.

    Returns:
        str: A welcome message or HTML content for the home page.
    '''
    return render_template('home.html')


# Endpoint for interactive heat map
@app.route(map_node)
def api_map():
    '''
    Returns restaurant markers with details for an interactive map.

    Returns:
        flask.Response: A JSON response containing map data.
    '''
    stmt = (
        select(
            Restaurants.id
            ,Restaurants.name
            ,Restaurants.lat
            ,Restaurants.lng
            ,Boroughs.borough
            ,Cuisines.cuisine
            ,Restaurants.inspection_date
        ).join(
            Boroughs
            ,Boroughs.borough_id == Restaurants.borough_id
        ).join(
            Cuisines
            ,Cuisines.cuisine_id == Restaurants.cuisine_id
        )
    )
    results = execute_query(stmt)
    data = [
        {
            'id': r.id,
            'name': r.name,
            'lat': r.lat,
            'lng': r.lng,
            'borough': r.borough,
            'cuisine': r.cuisine,
            'inspection_date': dt.date.isoformat(r.inspection_date)
        }
    for r in results]
    desc = 'Retrieves restaurant details for interactive heat map.'
    data_nest = forge_json(map_node, data, desc)
    return jsonify(data_nest)


# Endpoint for bar chart
@app.route(topCuisines_node)
def api_topCuisines():
    '''
    Retrieves aggregated counts for cuisines in a given borough.

    Query Parameters:
        borough (str): The name of the borough to filter cuisines by.

    Returns:
        flask.Response: A JSON response containing cuisine counts for the specified borough.
    '''
    boro_param = request.args.get('borough')
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
    results = execute_query(stmt)
    data = [
        {
            'cuisine': r.cuisine,
            'count': r.count
        } 
        for r in results]
    desc = 'Retrieves aggregated counts for cuisines in given borough.'
    params = {'borough': boro_param}
    data_nest = forge_json(topCuisines_node, data, desc, params)
    return jsonify(data_nest)


# Endpoint for total pie chart
@app.route(cuisineDist_node)
def api_cuisine_pie():
    '''
    Returns the percentage distribution of different ethnic cuisines across the city.

    Returns:
        flask.Response: A JSON response containing cuisine distribution data.
    '''
    stmt_total = select(func.count(Restaurants.id))
    total = execute_query(stmt_total)[0][0]
    stmt = (
        select(
            Cuisines.cuisine.label('cuisine')
            ,func.count(Restaurants.id).label('count')
        ).join(
            Restaurants
            ,Restaurants.cuisine_id == Cuisines.cuisine_id
        ).group_by(Cuisines.cuisine)
    )
    results = execute_query(stmt)
    data = [
        {
            'cuisine': r.cuisine
            ,'count': r.count
            ,'percent': (r.count / total * 100)
        }
    for r in results]
    desc = 'Retrieves percent distribution of all cuisines across NYC.'
    data_nest = forge_json(cuisineDist_node, data, desc)
    return jsonify(data_nest)


@app.route(boroughSummary_node)
def api_borough_summary():
    stmt = (
        select(
            Boroughs.borough.label('borough')
            ,func.count(Restaurants.id).label('restaurant_count')
            ,Boroughs.population.label('population')
        ).join(
            Restaurants
            ,Restaurants.borough_id == Boroughs.borough_id
        ).group_by(Boroughs.borough)
    )
    results = execute_query(stmt)
    data = [
        {
            'borough': r.borough
            ,'restaurant_count': r.restaurant_count
            ,'population': r.population
        }
    for r in results]
    desc = 'Retrieves summary statistics per each borough.'
    data_nest = forge_json(boroughSummary_node, data, desc)
    return jsonify(data_nest)



if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')