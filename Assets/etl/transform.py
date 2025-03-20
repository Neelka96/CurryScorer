import pandas as pd
from pathlib import Path
from typing import Callable

# TRANSFORMATIONS

# Cleaner helper
def clean_helper(df: pd.DataFrame) -> pd.DataFrame:
    '''Recieves pandas DataFrame as input, returns de-duplicated and datetime type correct DataFrame.'''

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

    return df.copy()

def grab_list(posix_url: Path | str) -> list:
    '''Reader for various lists that will be used to filter dataframe prenormalization'''
    posix_url = Path(posix_url)
    # Checking for path existence first
    if posix_url.exists():
        try:
            with open(posix_url, 'r') as file:
                return [line.strip('\n') for line in file]
        except Exception as e:
            print(f'ERROR: {e}')
            return -1
    else:
        return -1
    
def set_list(posix_url: Path | str, new_list: list) -> list:
    '''Writer for various lists that will be used to filter dataframe prenormalization'''
    new_list = [f'{item}\n' for item in new_list]
    posix_url = Path(posix_url)
    try:
        with open(posix_url, 'w') as file:
            file.writelines(new_list)
        return 0
    except Exception as e:
        print(f'ERROR: {e}')
        return -1

# -------------------------------------------------------------------------------------------

def clean_df(
        df: pd.DataFrame = None
        ,drop_dict: dict[str:list] = None
        ,keep_dict: dict[str:list] = None
    ) -> pd.DataFrame:
    '''Cleans pandas DataFrame by calling `clean_helper()` and dropping/keeping only objects passed into correctly designated arguments.'''

    # Calls clean_helper() on df to drop duplicates, sort columns, and correct datetime datetype
    if df:
        df = clean_helper(df)

    # Performs filtering loops by dictionary passed into argument (if no arguments -> no filtering occurs)
    # If in drop_dict then drop it
    if drop_dict:
        for name, dropList in drop_dict:
            dropLogic = ~df[name].isin(dropList)
            df = df.loc[dropLogic].copy()

    # If in keep_dict then keep it
    if keep_dict:
        for name, keepList in keep_dict:
            keepLogic = df[name].isin(keepList)
            df = df.loc[keepLogic].copy()

    return df.copy()


def create_dict(
        ref_list: list
        ,trans_func: Callable[[str], str]
    ) -> dict:
    '''Takes in a reference list to create alias identifiers for, along with function used to map new aliases.'''

    # Dictionary comprehension used to apply function to each item as it's placed in dictionary
    norm_dict = {item : trans_func(num) for num, item in enumerate(ref_list, start = 1)}
    return norm_dict

# CONSTANT
BOROUGHS = ['Manhattan', 'Bronx', 'Brooklyn', 'Queens', 'Staten Island']
def map_borough(
        boros: list = BOROUGHS
        ,denorm_df: pd.DataFrame = None
    ) -> dict:
    '''Wrapper for `create_dict()` to create a borough dictionary with either default, custom, or DataFrame derived list.'''
    # Checks for argument inputs
    if denorm_df:
        try:
            boros = denorm_df['borough'].unique()
        except Exception as e:
            print(f'Sorry, the following error has occured: \n{e}')
            return -1
    return create_dict(boros, lambda num: f'B{num}')


def map_cuisine(
        posix_url: Path | str = None
        ,cuisines: list = None
        ,denorm_df: pd.DataFrame = None
    ) -> dict:
    '''Wrapper for `create_dict()` to create cuisine dictionary with custom or DataFrame derived list. Default uses static list created using project criteria.'''
    # Checks for argument inputs
    if posix_url:
        cuisines = grab_list(posix_url)
    elif cuisines:
        pass
    elif denorm_df:
        try:
            cuisines = denorm_df['cuisine'].unique()
        except Exception as e:
            print(f'ERROR: \n{e}')
            return -1
    try:
        return create_dict(cuisines, lambda num: f'C{num}')
    except Exception as e:
        print(f'ERROR: \n{e}')
        return -1


def create_ref_table(
        trans_dict: dict
        ,target_col: str
        ,new_col: str
    ) -> pd.DataFrame:
    # DF to hold new table
    new_col = f'{target_col}_id'
    new_table = pd.DataFrame(
        {
            new_col: trans_dict.values(),
            target_col: trans_dict.keys()
        }
    )
    return new_table.copy()


def norm_table(
        denorm_df: pd.DataFrame
        ,trans_dict: dict
        ,target_col: str
        ,new_col: str
    ) -> pd.DataFrame:
    '''Used to normalize main table after extraction and reference tables have been built.'''
    # Map dataframe target column values to dictionary containing new values
    denorm_df[target_col] = denorm_df[target_col].map(trans_dict)
    return denorm_df.rename(columns = {target_col: new_col}).copy()

# --------------------------------------------------------------------------------------------------------

# Largest Abstractions in this file

def forge_boroughs(
        map: dict = None
        ,boro_list: list = None
        ,denorm_df: pd.DataFrame = None
    ) -> pd.DataFrame:
    '''If using a df, please make sure it's incoming denormalized df, as it will search for original column'''
    # Checking for type of input
    if map:
        boro_dict = map
    elif boro_list:
        boro_dict = map_borough(boros = boro_list)
    elif denorm_df:
        boro_dict = map_borough(df = denorm_df)
    else:
        boro_dict = map_borough()
    # Call and return a created reference table for boroughs using set variables
    return create_ref_table(boro_dict, 'borough', 'borough_id')


def forge_cuisines(
        map: dict = None
        ,posix_url: Path = None
        ,cuisine_list: list = None
        ,denorm_df: pd.DataFrame = None
    ) -> pd.DataFrame:
    # Checking for type of input
    if map:
        cuisine_dict = map
    elif posix_url:
        cuisine_dict = map_cuisine(posix_url= posix_url)
    elif cuisine_list:
        cuisine_dict = map_cuisine(cuisines = cuisine_list)
    elif denorm_df:
        cuisine_dict = map_cuisine(df = denorm_df)
    # Call and return a created reference table for boroughs using set variables
    return create_ref_table(cuisine_dict, 'cuisine', 'cuisine_id')

def transformation(
        df: pd.DataFrame
        ,posix_url: Path
        ,drop_dict: dict[str:list] = None
        ,keep_dict: dict[str:list] = None
        ,forge_all: bool = False
    ) -> pd.DataFrame:

    boro_dict = map_borough()
    cuisine_dict = map_cuisine(posix_url)
    
    df = clean_df(df, drop_dict = drop_dict, keep_dict = keep_dict)
    
    if forge_all:
        borough_df = forge_boroughs(map = boro_dict)
        cuisine_df = forge_cuisines(map = cuisine_dict)
        norm_df = norm_table(df, boro_dict, 'borough', 'borough_id')
        norm_df = norm_table(norm_df, cuisine_dict, 'cuisine', 'cuisine_id')
        return norm_df.copy(), borough_df.copy(), cuisine_df.copy()
    else:
        norm_df = norm_table(df, boro_dict, 'borough', 'borough_id')
        norm_df = norm_table(norm_df, cuisine_dict, 'cuisine', 'cuisine_id')
        return norm_df.copy()


if __name__ == '__main__':
    pass