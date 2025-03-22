# Import dependencies
from flask import request


# Automatic Metadata Creation
# ---------------------------
def forge_metadata(route, length, desc, params):
    metadata = {
        'current_route': route
        ,'home_route': request.host 
        ,'data_points': length
        ,'info': desc
        ,'params': params
        ,'format': 'json'
    }
    return metadata

# Nests metadata and results together in one object 
def format_json(route, nest, desc = 'None', params = 'None'):
    json_api = {
        'metadata': forge_metadata(route, len(nest), desc, params)
        ,'results': nest
    }
    return json_api


home_html = (
    '<head>'
    '</head>'
    '<body>'
        '<h1>Welcome!</h1>'
    '</body>'
)

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')