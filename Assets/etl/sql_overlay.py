import dohmh_ETL as etl


# SQL LEVEL ABSTRACTION LAYER (LOADING)

def Load_DOHMH_ETL(subroutine: str = 'full') -> list[etl.pd.DataFrame]:
    if subroutine == 'full':
        main_df = etl.Extraction('dohmh')
        fastFood_path = etl.Path('../csv_files/clean/fastfood.csv')
        return etl.Transformation(main_df, fastFood_path)
    elif subroutine == 'update':
        main_df = etl.Extraction('dohmh')

def get_(table_name):
    

if __name__ == '__main__':
    tables = [*Load_DOHMH_ETL('full')]
    print(tables[2])