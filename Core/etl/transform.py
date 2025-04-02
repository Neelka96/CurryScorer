# Import dependencies
import pandas as pd
from collections.abc import Callable

# Bring in custom logger
from Core.log_config import init_log
log = init_log(__name__)


def create_dict(
        ref_list: list[str]
        ,translation: Callable[[int], str]
        ) -> dict[str, str]:
    '''Used to create lightweight reference dictionaries for transformations.

    Args:
        ref_list (list[str]): Constants used for mappings.
        translation (Callable[[int], str]): Function to map against constants.

    Returns:
        dict[str, str]: Mapped dictionary with reference ids.
    '''
    log.debug('Creating dictionary for reference table.')
    # Dictionary comprehension used to apply function to each item as it's placed in dictionary
    return {item : translation(num) for num, item in enumerate(ref_list, start = 1)}


def create_ref_table(
        mapping: dict[str, str]
        ,target_col: str
    ) -> pd.DataFrame:
    '''Readies reference/parent table for SQL insertion.

    Args:
        mapping (dict[str, str]): Mapping from `create_dict()`.
        target_col (str): Primary key column to be created.

    Returns:
        pd.DataFrame: 2 column table with unique IDs.
    '''
    log.debug('Creating reference table.')
    # Adds 'id' to target column's name to create reference ID column
    new_col = f'{target_col}_id'

    # Initializes the dataframe using dictionary pairs for values
    return pd.DataFrame(
        {
            new_col: mapping.values(),
            target_col: mapping.keys()
        }
    )


def clean_df(
        df: pd.DataFrame
        ,junkFood_names: list[str]
        ,ethnic_cuisines: list[str]
    ) -> pd.DataFrame:
    '''Cleanses DataFrame using predefined metrics.

    Args:
        df (pd.DataFrame): Data to be cleaned.
        junkFood_names (list[str]): Static list of names to remove
        ethnic_cuisines (list[str]): Static list of cuisines to keep.

    Returns:
        pd.DataFrame: Cleaned dataframe.
    '''
    log.debug('Cleaning dataframe using hard-logic.')
    # Bulk cleaning operations in one go 
    return (
        df
            .assign(inspection_date = pd.to_datetime(df['inspection_date']))    # Convert to datetime
            .sort_values('inspection_date', ascending = False)  # Sort by inspection date
            .drop_duplicates(subset = ['id'], keep = 'first')   # Drop duplicate locations keeping most recent
            .loc[:, ['id', 'name', 'borough', 'cuisine', 'inspection_date', 'lat', 'lng']]  # Re-arrange columns
            .pipe(lambda x: x[~x['name'].isin(junkFood_names) & x['cuisine'].isin(ethnic_cuisines)])    # Drop by static lists
            .reset_index(drop = True)
    )


def normalize_table(
        denorm_df: pd.DataFrame
        ,mapping: dict[str, str]
        ,target_col: str
    ) -> pd.DataFrame:
    '''Normalizes table using reference/parent table.

    Args:
        denorm_df (pd.DataFrame): Denormalized data.
        mapping (dict[str, str]): Reference mapping from `create_dict()`.
        target_col (str): New normalized column name.

    Returns:
        pd.DataFrame: Table normalized via one metric.
    '''
    log.debug('Normalizing dataframe to reference tables.')
    # Map dataframe target column values to dictionary containing new values
    denorm_df[target_col] = denorm_df[target_col].map(mapping)

    # Rename and return the edited dataframe
    return denorm_df.rename(columns = {target_col: f'{target_col}_id'})


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')