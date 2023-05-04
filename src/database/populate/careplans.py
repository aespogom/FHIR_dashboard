'''
    This module contains the logic to create and populate CAREPLANS SQL database table
    ATTENTION! Running this script will delete all existing tables and populate them with
    the our predefined data stored in data/synthea_output/csv.
    All changes will be lost.
'''

import database_connection
import pandas as pd
import numpy as np

## CAREPLANS
def populate_table(reset_table: bool):
    if reset_table:
        table_careplans = '''
            IF OBJECT_ID('careplans') IS NOT NULL
                DROP TABLE careplans;  
            CREATE TABLE careplans (
                START date,
                STOP date,
                ID UNIQUEIDENTIFIER not null,
                PATIENT UNIQUEIDENTIFIER not null,
                ENCOUNTER UNIQUEIDENTIFIER,
                CODE integer,
                DESCRIPTION nvarchar(150),
                REASONCODE integer,
                REASONDESCRIPTION nvarchar(150)
                primary key (ID)
            );'''

        database_connection.execute_query(table_careplans)

    data = pd.read_csv('./src/database/data/synthea_output/csv/careplans.csv')   
    df = pd.DataFrame(data)
    df = df.replace(np.nan,'',regex = True)
    df['START']= pd.to_datetime(df['START'], errors='ignore')
    df['STOP']= pd.to_datetime(df['STOP'], errors='ignore')
    
    for row in df.itertuples():
        populate_careplans = '''
            INSERT INTO careplans 
            (ID,START,STOP,PATIENT,ENCOUNTER,CODE,DESCRIPTION,REASONCODE,REASONDESCRIPTION)
            VALUES (?,?,?,?,?,?,?,?,?)
        '''
        database_connection.execute_query(populate_careplans, tuple(row[1:]))

