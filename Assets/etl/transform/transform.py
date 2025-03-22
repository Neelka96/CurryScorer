import pandas as pd
from typing import Callable


# TRANSFORMATION HELPERS

# Cleaner helper
def clean_helper(df: pd.DataFrame) -> pd.DataFrame:
    '''Recieves pandas DataFrame as input, returns de-duplicated and datetime type correct DataFrame.'''

    # Correcting date type --> datetime (doesn't need times or tz info)
    df['inspection_date'] = pd.to_datetime(df['inspection_date'])

    # Sort by inspection date for most recent dates then drop duplicate ids and keep most recent
    df = (df
            .sort_values('inspection_date', ascending = False)
            .drop_duplicates(subset = ['id'], keep = 'first'))

    # Reorder to correct columns
    df = df[
        ['id', 'name', 'borough', 'cuisine', 'inspection_date', 'lat', 'lng']
    ].reset_index(drop = True)

    return df


def clean_df(
        df: pd.DataFrame
        ,drop_dict: dict[str:list] = None
        ,keep_dict: dict[str:list] = None
    ) -> pd.DataFrame:
    '''Cleans pandas DataFrame by calling `clean_helper()` and dropping/keeping only objects passed into correctly designated arguments.'''

    # Calls clean_helper() on df to drop duplicates, sort columns, and correct datetime datetype
    try:
        df = clean_helper(df)
    except Exception as e:
        raise RuntimeError(f'Could not process clean_helper on df: {e}')

    # Performs filtering loops by dictionary passed into argument (if no arguments -> no filtering occurs)
    mask = pd.Series(True, index = df.index)
    if drop_dict:
        mask &= [~df[col].isin(dropList) for col, dropList in drop_dict.items()]
    if keep_dict:
        mask &= [df[col].isin(keepList) for col, keepList in keep_dict.items()]

    return df[mask]


def create_dict(ref_list: list, translation: Callable[[int], str]) -> dict:
    '''Takes in a reference list to create alias identifiers for, along with function used to map new aliases.'''

    # Dictionary comprehension used to apply function to each item as it's placed in dictionary
    norm_dict = {item : translation(num) for num, item in enumerate(ref_list, start = 1)}
    return norm_dict


def create_ref_table(
        mapping: dict[str, str]
        ,target_col: str
        ,new_col: str
    ) -> pd.DataFrame:
    '''
    Creates new reference table using a mapping, a column name, and adding `_id`.
    '''
    new_col = f'{target_col}_id'
    new_table = pd.DataFrame(
        {
            new_col: mapping.values(),
            target_col: mapping.keys()
        }
    )
    return new_table


def normalizeTable(
        denorm_df: pd.DataFrame
        ,mapping: dict[str, str]
        ,target_col: str
        ,new_col: str
    ) -> pd.DataFrame:
    '''Used to normalize main table with reference mappings on a target column.'''
    # Map dataframe target column values to dictionary containing new values
    denorm_df[target_col] = denorm_df[target_col].map(mapping)
    return denorm_df.rename(columns = {target_col: new_col})


if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')