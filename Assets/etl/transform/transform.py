# Import dependencies
import pandas as pd
from collections.abc import Callable


# TRANSFORMATION HELPERS

# Cleaner helper
def clean_helper(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Helper function for clean_df(), performs necessary cleaning operations known to be needed for particular dataset.

    Args:
        df (pd.DataFrame): A pandas dataframe to be cleaned by pre-set methods.

    Returns:
        pd.DataFrame: A pandas Dataframe with datetime correction, de-duplication, and column re-ordering.
    '''
    # Correcting date type --> datetime (doesn't need times or tz info)
    df['inspection_date'] = pd.to_datetime(df['inspection_date'])

    # Sort by inspection date for most recent dates then drop duplicate ids and keep most recent
    df = (df
            .sort_values('inspection_date', ascending = False)
            .drop_duplicates(subset = ['id'], keep = 'first'))

    # Reorder to correct columns, and return
    return df[['id', 'name', 'borough', 'cuisine', 'inspection_date', 'lat', 'lng']].reset_index(drop = True)


def clean_df(
        df: pd.DataFrame
        ,junkFood_names: list[str]
        ,ethnic_cuisines: list[str]
    ) -> pd.DataFrame:
    '''
    Cleans pandas DataFrame by calling `clean_helper()` and dropping/keeping only objects passed into correctly designated arguments.

    Args:
        df (pd.DataFrame):
        junkFood_names (list[str]):
        ethnic_cuisines (list[str]):

    Returns:
        pd.DataFrame:
    '''
    # Tries to call clean_helper() on df to drop duplicates, sort columns, and correct datetime datetype
    try:
        df = clean_helper(df)

    # Raises on error when df can't be cleaned for some reason
    except Exception as e:
        raise RuntimeError(f'Could not process clean_helper on df: {e}')
    
    # Creates boolean mask using lists passed (already derived from constants, no point in re-declaring them again)
    return df[~df['name'].isin(junkFood_names) & df['cuisine'].isin(ethnic_cuisines)]


def create_dict(
        ref_list: list[str]
        ,translation: Callable[[int], str]
        ) -> dict[str, str]:
    '''
    Creates a dictionary from a reference list using a translation function.

    Args:
        ref_list (list[str]): A list of reference items, typically boroughs or cuisines.
        translation (Callable[[int], str]): A function to generate dictionary values, typically reference IDs.

    Returns:
        dict[str, str]: A dictionary with items from the reference list as keys and translated values.
    '''
    # Dictionary comprehension used to apply function to each item as it's placed in dictionary
    return {item : translation(num) for num, item in enumerate(ref_list, start = 1)}


def create_ref_table(
        mapping: dict[str, str]
        ,target_col: str
    ) -> pd.DataFrame:
    '''
    Creates a reference table using a mapping, a target column, and a new column name.

    Args:
        mapping (dict[str, str]): A mapping of keys to values for the reference table.
        target_col (str): The name of the target column.

    Returns:
        pd.DataFrame: A DataFrame representing the reference table.
    '''
    # Adds 'id' to target column's name to create reference ID column
    new_col = f'{target_col}_id'

    # Initializes the dataframe using dictionary pairs for values
    return pd.DataFrame(
        {
            new_col: mapping.values(),
            target_col: mapping.keys()
        }
    )


def normalizeTable(
        denorm_df: pd.DataFrame
        ,mapping: dict[str, str]
        ,target_col: str
    ) -> pd.DataFrame:
    '''
    Normalizes a DataFrame by mapping a targeted columns values to reference IDs, and renaming the column. Assumes integrity of reference tables when making this edit.

    Args:
        denorm_df (pd.DataFrame): The freshly created DataFrame to be normalized.
        mapping (dict[str, str]): A mapping of old values to new values. (Values independent of table replaced with reference IDs)
        target_col (str): The name of the column being normalized.

    Returns:
        pd.DataFrame: The normalized DataFrame with new column names.
    '''
    # Map dataframe target column values to dictionary containing new values
    denorm_df[target_col] = denorm_df[target_col].map(mapping)

    # Rename and return the edited dataframe
    return denorm_df.rename(columns = {target_col: f'{target_col}_id'})



if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')