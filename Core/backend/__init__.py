# Import dependencies
from sqlalchemy import func, select
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
from werkzeug.middleware.proxy_fix import ProxyFix
import datetime as dt

# Import subpackage dependencies
from . import backend as api
from . database import Restaurants, Boroughs, Cuisines, Session
import config as C

#################################################
# Flask Setup
#################################################
app = Flask(__name__, template_folder = C.TEMPLATE_DIR)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto = 1, x_host = 1)
CORS(app, resources={r"/api/*": {"origins": "*"}}, send_wildcard = True)
app.json.sort_keys = False
app.url_map.strict_slashes = False

# Endpoint Declarations
# heat_map_node = '/api/v1.0/map/'
# top_cuisines_node = '/api/v1.0/top-cuisines/'
# cuisine_dist_node = '/api/v1.0/cuisine-distributions/'
# borough_summary_node = '/api/v1.0/borough-summaries/'


#################################################
# Flask Endpoints
#################################################

# Endpoint for home
@app.route('/')
# @cross_origin(origins="*")
def home():
    '''
    Home endpoint for the API.

    Returns:
        str: A welcome message or HTML content for the home page.
    '''
    return render_template('home.html')


# Endpoint for interactive heat map
@app.route('/api/v1.0/map/')
# @cross_origin(origins="*")
def api_map():
    '''
    Returns restaurant markers with details for an interactive map.
    Each marker includes name, latitude, longitude, borough, cuisine, etc.

    Returns:
        flask.Response: A JSON response containing heat map data.
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
    data_nest = api.forge_json('/api/v1.0/map/', data, desc)
    return jsonify(data_nest)


# Endpoint for bar chart
@app.route('/api/v1.0/top-cuisines/')
# @cross_origin(origins="*")
def api_topCuisines():
    '''
    Retrieves aggregated counts for cuisines in a given borough.

    Query Parameters:
        borough (str): The name of the borough to filter cuisines by.

    Returns:
        flask.Response: A JSON response containing cuisine counts for the specified borough.
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
    data_nest = api.forge_json('/api/v1.0/top-cuisines/', data, desc, params)
    return jsonify(data_nest)


# Endpoint for total pie chart
@app.route('/api/v1.0/cuisine-distributions/')
# @cross_origin(origins="*")
def api_cuisine_pie():
    '''
    Returns the percentage distribution of different ethnic cuisines across the city.

    Returns:
        flask.Response: A JSON response containing cuisine distribution data.
    '''
    with Session() as session:
        stmt_total = select(func.count(Restaurants.id))
        total = session.scalars(stmt_total).one()

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
    data_nest = api.forge_json('/api/v1.0/cuisine-distributions/', data, desc)
    return jsonify(data_nest)


@app.route('/api/v1.0/borough-summaries/')
# @cross_origin(origins="*")
def api_borough_summary():
    with Session() as session:
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
        results = session.execute(stmt).all()
        data = [
            {
                'borough': r.borough
                ,'restaurant_count': r.restaurant_count
                ,'population': r.population
            }
        for r in results]
    desc = 'Retrieves summary statistics per each borough.'
    data_nest = api.forge_json('/api/v1.0/borough-summaries/', data, desc)
    return jsonify(data_nest)



if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')