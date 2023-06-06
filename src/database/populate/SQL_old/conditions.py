'''
    This module contains the logic to create and populate CONDITIONS SQL database table
    ATTENTION! Running this script will delete all existing tables and populate them with
    the our predefined data stored in data/synthea_output/csv.
    All changes will be lost.
'''

import database_connection
import pandas as pd
import numpy as np


## CONDITIONS
def populate_table(reset_table: bool):
    if reset_table:
        table_conditions= '''
            IF OBJECT_ID('conditions') IS NOT NULL
                DROP TABLE conditions;  
            CREATE TABLE conditions (
                START date,
                STOP date,
                PATIENT UNIQUEIDENTIFIER not null,
                ENCOUNTER UNIQUEIDENTIFIER,
                CODE integer,
                DESCRIPTION nvarchar(150),
                primary key (PATIENT, ENCOUNTER, START, CODE)
            );'''

        database_connection.execute_query(table_conditions)

    data = pd.read_csv('./src/database/data/synthea_output/csv/conditions.csv')   
    df = pd.DataFrame(data)
    df = df.replace(np.nan,'',regex = True)
    df['START']= pd.to_datetime(df['START'], errors='ignore')
    df['STOP']= pd.to_datetime(df['STOP'], errors='ignore')
    
    for row in df.itertuples():

        populate_conditions = '''
            INSERT INTO conditions 
            (START,STOP,PATIENT,ENCOUNTER,CODE,DESCRIPTION)
            VALUES (?,?,?,?,?,?)
            '''
        database_connection.execute_query(populate_conditions, tuple(row[1:]))

