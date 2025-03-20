# Import the dependencies.
import pandas as pd
import requests
import io
import datetime as dt
from pathlib import Path

# -------------------------------------------------------------------------------------

# # EXTRACTION

# def get_df(url: str, params: dict = None) -> pd.DataFrame:
#     # API Call itself using socrata (SODA) querying
#     response = requests.get(url, params)

#     # Using io.StringIO to create pseudo CSV file for reading
#     csv = io.StringIO(response.content.decode('utf-8'))
#     return pd.read_csv(csv)


# def where_filter(numYears: int = 2) -> str:
#     # Build filters for date (default 2 years) and no nulls for cuisine, lat, or lng
#     dateLimit = (dt.datetime.now() - dt.timedelta(days = numYears * 365)).isoformat()
#     filter_dt = f'inspection_date > "{dateLimit}"'
#     notNull = 'IS NOT NULL'
#     filter_NA = \
#         f'cuisine {notNull} AND lat {notNull} AND lng {notNull}'
    
#     # Init full filters for API call with limit
#     return f'{filter_dt} AND {filter_NA}'


# MAX_LIMIT = 200000
# def Extraction(dataSet: str, limit: str = MAX_LIMIT) -> pd.DataFrame:
#     # Conditional switch for 2 datasets
#     if dataSet == 'dohmh':
#     # Build select statement with aliases
#         select = (
#             'camis AS id,'
#             'dba AS name,'
#             'boro AS borough,'
#             'cuisine_description AS cuisine,'
#             'inspection_date,'
#             'latitude AS lat,'
#             'longitude AS lng'
#         )
#         # Parameters to send with API Call
#         params = {
#             '$select': select,
#             '$where': where_filter(),
#             '$limit': limit
#         }
#         url = 'https://data.cityofnewyork.us/resource/43nn-pn8j.csv'

#     elif dataSet == 'fast_food':
#         # Build select statement with aliases
#         select = (
#             'restaurant AS name,'
#             'Item_Name AS item,'
#             'Food_Category AS cat'
#         )
#         # Parameters to send with API Call
#         params = {
#             '$select': select,
#             '$limit': limit
#         }
#         url = 'https://data.cityofnewyork.us/resource/qgc5-ecnb.csv'

#     # Return extracted and file-formatted data
#     return get_df(url, params)

# # -------------------------------------------------------------------------------------

# # TRANSFORMATION

# def clean_df(df: pd.DataFrame, name_set: list, cuisine_set: list) -> pd.DataFrame:
#     # Correcting date type --> datetime (doesn't need times or tz info)
#     df['inspection_date'] = pd.to_datetime(df['inspection_date'])

#     # Groupy by to resolve outdated records (grab most recent ones only)
#     uniqueLocs = df.groupby('id')['inspection_date'].max().reset_index(drop = False)
#     df = uniqueLocs.merge(df, how = 'left').copy()

#     # Multiple most recent records per id so drop exact duplicates
#     df = df.drop_duplicates(keep = 'last')

#     # Reorder to correct columns
#     df = df[
#         ['id', 'name', 'borough', 'cuisine', 'inspection_date', 'lat', 'lng']
#     ].reset_index(drop = True)

#     # Save pandas bool logic to variable for easy access
#     dropLogic = (~df['name'].isin(name_set) | ~df['cuisine'].isin(cuisine_set))

#     return df.loc[dropLogic]



# def normalize(df: pd.DataFrame, ref_list: list, target_col: str, trans_func) -> pd.DataFrame:
#     # Create normalized dictionary
#     norm_dict = {boro : trans_func(num) for num, boro in enumerate(ref_list, start = 1)}

#     # DF to hold new table
#     new_col = f'{target_col}_id'
#     new_table = pd.DataFrame(
#         {
#             new_col: norm_dict.values(),
#             target_col: norm_dict.keys()
#         }
#     )

#     # Mapping borough names to new id (mod DF by ref)
#     df[target_col] = df[target_col].map(norm_dict)
#     df = df.rename(columns = {target_col: new_col})

#     # Return new table from normalization
#     return new_table


# def Transformation(df: pd.DataFrame, csvPath: Path, force_download: bool = False) -> list[pd.DataFrame]:
#     # Build drop lists
#     if not csvPath.exists() or force_download:
#         drop_names = Extraction('fast_food')['name'].unique()
#         pd.Series({'name': drop_names}).to_csv(csvPath, header = True, index = False)
    
#     drop_names = pd.read_csv(csvPath)
    
#     # Creating by analyzing available cuisine types in orig table
#     drop_cuisines = [
#         'Bakery Products/Desserts', 'Sandwiches', 'Frozen Desserts', 'Hotdogs', 'Donuts', 'Other',
#         'Coffee/Tea', 'Seafood', 'Bottled Beverages', 'Hamburgers', 'Chicken', 
#         'Bagels/Pretzels', 'Pancakes/Waffles', 'Vegetarian', 'Juice, Smoothies, Fruit Salads',
#         'Fusion', 'Salads', 'Sandwiches/Salads/Mixed Buffet', 'Hotdogs/Pretzels', 
#         'Vegan', 'Californian', 'Soups/Salads/Sandwiches', 'Soups', 'Fruits/Vegetables', 
#         'Nuts/Confectionary', 'Not Listed/Not Applicable', 'Chimichurri'
#     ]
#     # Call cleaning function
#     df = clean_df(df, drop_names, drop_cuisines).copy()

#     return df

# def norm_boroughs(df: pd.DataFrame):
#     # Normalizing borough name
#     boros = ['Manhattan', 'Bronx', 'Brooklyn', 'Queens', 'Staten Island']
#     boro_df = normalize(df, boros, 'borough', lambda boro: f'B{boro}')

#     return boro_df

# def norm_cuisines(df: pd.DataFrame):
#     # Normalizing cuisine type
#     cuisines = df['cuisine'].unique()
#     cuisine_df = normalize(df, cuisines, 'cuisine', lambda cuisine: f'C{cuisine}')

#     return cuisine_df

# # -------------------------------------------------------------------------------------

# Execution script (not for use)
if __name__ == '__main__':
    print('DOHMH ETL Script - Not for executable use')