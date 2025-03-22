from sqlalchemy import func, select
from flask import Flask, jsonify, request, abort
from Assets.etl.database import Restaurants, Boroughs, Cuisines, Session, engine
import datetime as dt

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Routes
map_node = '/api/v1.0/map'
top_cuisines = '/api/v1.0/top-cuisines/'
cuisine_dist = '/api/v1.0/cuisine-distribution'


#################################################
# Flask Endpoints
#################################################

# Endpoint for home
@app.route('/')
def home():
    return (
        '<head>'
        '</head>'
        '<body>'
            '<h1>Welcome!</h1>'
        '</body>'
    )


# Endpoint for interactive heat map
@app.route(map_node)
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
    return jsonify(data)


@app.route(top_cuisines)
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
    return jsonify(data)


@app.route(cuisine_dist)
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
        return jsonify(data)



if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')