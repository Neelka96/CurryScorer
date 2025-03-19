# Import the dependencies.
import pandas as pd
import requests
import io
import datetime as dt

MAX_LIMIT = 200000

def get_df(url, params = None):
    # API Call itself using socrata (SODA) querying
    response = requests.get(url, params)

    # Using io.StringIO to create pseudo CSV file for reading
    csv = io.StringIO(response.content.decode('utf-8'))
    return pd.read_csv(csv)


def where_filter(numYears = 2):
    # Build filters for date (default 2 years) and no nulls for cuisine, lat, or lng
    dateLimit = (dt.datetime.now() - dt.timedelta(days = numYears * 365)).isoformat()
    filter_dt = f'inspection_date > "{dateLimit}"'
    notNull = 'IS NOT NULL'
    filter_NA = \
        f'cuisine {notNull} AND lat {notNull} AND lng {notNull}'
    
    # Init full filters for API call with limit
    return f'{filter_dt} AND {filter_NA}'


def get_dohmh_df(limit = MAX_LIMIT):
    # Build select statement with aliases
    select = (
        'camis AS id,'
        'dba AS name,'
        'boro AS borough,'
        'cuisine_description AS cuisine,'
        'inspection_date,'
        'latitude AS lat,'
        'longitude AS lng'
    )
    # Parameters to send with API Call
    url = 'https://data.cityofnewyork.us/resource/43nn-pn8j.csv'
    params = {
        '$select': select,
        '$where': where_filter(),
        '$limit': limit
    }
    return get_df(url, params)


def get_fastFood_df(limit = MAX_LIMIT):
    select = (
        'restaurant AS name,'
        'Item_Name AS item,'
        'Food_Category AS cat'
    )
    params = {
        '$select': select,
        '$limit': limit
    }

    url = 'https://data.cityofnewyork.us/resource/qgc5-ecnb.csv'
    return get_df(url, params)



def cleaning(df : pd.DataFrame):
    # Correcting date type --> datetime (doesn't need times or tz info)
    df['inspection_date'] = pd.to_datetime(df['inspection_date'])

    # Groupy by to resolve outdated records (grab most recent ones only)
    uniqueLocs = df.groupby('id')['inspection_date'].max().reset_index(drop = False)
    df = uniqueLocs.merge(df, how = 'left').copy()

    # Multiple most recent records per id so drop exact duplicates
    df = df.drop_duplicates(keep = 'last')

    # Reorder to correct columns
    df = df[
        ['id', 'name', 'borough', 'cuisine', 'inspection_date', 'lat', 'lng']
    ].reset_index(drop = True)

    # Removing Fast Food Restaurants from DF
    fastFood_df = get_fastFood_df()
    fastFood_list = [*fastFood_df['name'].unique()]

    return df.loc[~df['name'].isin(fastFood_list)]


def normalize(df : pd.DataFrame):
    pass


def transform(df : pd.DataFrame):
    df = cleaning(df)
    
    # Data Normalization

    # Normalizing borough name
    boros = ['Manhattan', 'Bronx', 'Brooklyn', 'Queens', 'Staten Island']
    boro_dict = {boro : f'B{num}' for num, boro in enumerate(boros, start = 1)}

    # DF to hold new borough table
    boro_df = pd.DataFrame(
        {
            'borough_id': boro_dict.values(),
            'borough': boro_dict.keys()
        }
    )

    # Mapping borough names to new id
    df['borough'] = df['borough'].map(boro_dict)


    # Normalizing cuisine type and dropping eroneous types
    dropList = [
        'Bakery Products/Desserts', 'Sandwiches', 'Frozen Desserts', 'Hotdogs', 'Donuts', 'Other',
        'Coffee/Tea', 'Seafood', 'Bottled Beverages', 'Hamburgers', 'Chicken', 
        'Bagels/Pretzels', 'Pancakes/Waffles', 'Vegetarian', 'Juice, Smoothies, Fruit Salads',
        'Fusion', 'Salads', 'Sandwiches/Salads/Mixed Buffet', 'Hotdogs/Pretzels', 
        'Vegan', 'Californian', 'Soups/Salads/Sandwiches', 'Soups', 'Fruits/Vegetables', 
        'Nuts/Confectionary', 'Not Listed/Not Applicable', 'Chimichurri'
    ]
    df = df[~df['cuisine'].isin(dropList)]

    cuisines = df['cuisine'].unique()
    cuisines_dict = {cuisine : f'C{id}' for id, cuisine in enumerate(cuisines, start = 1)}

    # DF to hold new cuisine table
    cuisine_df = pd.DataFrame(
        {
            'cuisine_id': cuisines_dict.values(),
            'cuisine': cuisines_dict.keys()
        }
    )

    # Mapping cuisine types to new ID
    df['cuisine'] = df['cuisine'].map(cuisines_dict)

    # Renaming for Normalization
    df = df.rename(
        columns = {
            'borough': 'borough_id',
            'cuisine': 'cuisine_id'
        }
    )