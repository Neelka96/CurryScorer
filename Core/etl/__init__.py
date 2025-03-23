# Import dependencies
import pandas as pd
from pathlib import Path
from time import sleep

# Import package and subpackage requirements for core building
from . import extract as E
import config as C

def get_fastfoods(
        header: dict[str, str] = None
        ,csv_path: Path = C.FASTFOOD_CSV
        ,sleeping: int = C.SLEEP_TIME
        ) -> pd.DataFrame:
    '''
    Retrieves data from `fastfood.csv` if it exists, otherwise fetches it from the API.

    Args:
        csv_path (Path, optional): A path potentially referring to a CSV, holding data on fast food restaurant names.
        sleeping (int, optional): Seconds to sleep before requesting fast food API as this normally would happen after the first API call.

    Returns:
        pd.DataFrame: A DataFrame containing fast food data.

    Raises:
        RuntimeError: If the data cannot be extracted or saved.
    '''
    # Try to find or get fastfood data
    try:
        # Checks if csv path exists -> Returns df from csv
        if csv_path.exists():
            return pd.read_csv(csv_path)
        # Else extract a new fast_food csv (so sleep first between this and the first API call)
        else:
            # Save new df to prevent future API calls on this route and return df
            sleep(sleeping)
            return E.extraction('fast_food', header).to_csv(csv_path)
    except Exception as e:
        raise RuntimeError(f'Could not extract fast_food df: {e}')


# EOF 

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')