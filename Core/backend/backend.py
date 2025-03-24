# Import dependencies
from flask import request
from typing import Any


# Backend Helpers

# Automatic Metadata Creation
def forge_metadata(
        route: str
        ,length: int
        ,desc: str
        ,params: dict[str, str]
        ) -> dict[str, Any]:
    '''
    Creates dictionary of API request and response information, to be nested with API response.

    Args:
        route (str): The current API request route to be displayed.
        length (int): The length of API response to be displayed.
        desc (str): The written description of the API to be displayed.
        params (dict[str, str]): The parameters (if any) used to filter API request to be displayed.
    
    Returns:
        dict[str, Any]: A dictionary containing various data points about the API request and response.
    '''
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
def forge_json(
        route: str
        ,nest: dict[str, Any]
        ,desc: str = 'None'
        ,params: dict[str, str] = 'None'
        ) -> dict[str, Any]:
    '''
    Creates dictionary of nested API metadata and the API response. Outer wrapper that's actually called in script.
    Most arguments are abstracted or directly passed into forge_metadata() for displaying in JSON nest.

    Args:
        route (str): The current API request route to be fed to forge_metadata.
        nest (dict[str, Any]): Actual API resonse, currently only length is abstracted from it.
        desc (str): The written description of the API to be fed to forge_metadata.
        params (dict[str, str]): The parameters (if any) used to filter API request to be fed to forge_metadata.

    Returns:
        dict[str, Any]: A dictionary containing both the metadata and the API response ready for Flask's Jsonify().
    '''
    json_api = {
        'metadata': forge_metadata(route, len(nest), desc, params)
        ,'results': nest
    }
    return json_api


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')