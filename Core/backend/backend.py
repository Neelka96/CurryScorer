# LATEST CHANGELOG HERE:
#   - Adding contextlib @contextmanager decorator to handle session logic
#       + Therefore changing import of session to this location instead
#   - Adding sqlalchemy "Select" class for function hint
#   - Adding execute_query utility function to combine -> reduce boilerplate
#       


# Import dependencies
from contextlib import contextmanager
from flask import request
from sqlalchemy import Select, Row
from sqlalchemy.orm import Session as SessionClass
from collections.abc import Sequence, Generator

from .database import Session

# Backend Helpers

# Context management handler for sessions for centralized handling
@contextmanager
def get_session() -> Generator[SessionClass]:
    session = Session()
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()


# Utility For executing session requests
def execute_query(sql_stmt: Select) -> Sequence[Row]:
    with get_session() as session:
        return session.execute(sql_stmt).all()


# Automatic Metadata Creation
def forge_metadata(
        route: str
        ,length: int
        ,desc: str
        ,params: dict
        ) -> dict:
    '''
    Creates dictionary of API request and response information.

    Args:
        route (str): The current API request route.
        length (int): The length of the response.
        desc (str): The written description of the API endpoint.
        params (dict): The parameters used to filter request.
    
    Returns:
        dict: A dictionary containing metadata.
    '''
    return {
        'current_route': route
        ,'home_route': request.host
        ,'data_points': length
        ,'info': desc or None
        ,'params': params or {}
        ,'format': 'json'
    }

# Nests metadata and results together in one object 
def forge_json(
        route: str
        ,nest: dict
        ,desc: str
        ,params: dict = None
        ) -> dict:
    '''
    Creates dictionary of nested API metadata and the API response.

    Args:
        route (str): The current API request route.
        nest (dict): The actual resonse.
        desc (str): The written description of the API.
        params (dict, optional): The parameters used to filter request.

    Returns:
        dict: A dictionary containing API response and metadata.
    '''
    json_api = {
        'metadata': forge_metadata(route, len(nest), desc, params)
        ,'results': nest
    }
    return json_api


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')