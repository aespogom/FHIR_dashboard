'''
    This module contains the logic to create and populate OBSERVATIONS SQL database table
    ATTENTION! Running this script will delete all existing tables and populate them with
    the our predefined data stored in data/synthea_output/csv.
    All changes will be lost.
'''

import database_connection
import pandas as pd
import numpy as np


## OBSERVATIONS
def populate_table(reset_table: bool):
    if reset_table:
        table_observations= '''
            IF OBJECT_ID('observations') IS NOT NULL
                DROP TABLE observations;  
            CREATE TABLE observations (
                DATE date,
                PATIENT UNIQUEIDENTIFIER not null,
                ENCOUNTER UNIQUEIDENTIFIER,
                CATEGORY nvarchar(150),
                CODE nvarchar(150),
                DESCRIPTION nvarchar(150),
                VALUE nvarchar(150),
                UNITS nvarchar(150),
                TYPE nvarchar(150),
                primary key (PATIENT, ENCOUNTER, DATE, CODE)
            );'''

        database_connection.execute_query(table_observations)

    data = pd.read_csv('./src/database/data/synthea_output/csv/observations.csv')   
    df = pd.DataFrame(data)
    df = df.replace(np.nan,'',regex = True)
    df['DATE']= pd.to_datetime(df['DATE'], errors='ignore')
    for row in df.itertuples():

        populate_observations = '''
            INSERT INTO observations 
            (DATE,PATIENT,ENCOUNTER,CATEGORY,CODE,DESCRIPTION,VALUE,UNITS,TYPE)
            VALUES (?,?,?,?,?,?,?,?,?)
            '''
        database_connection.execute_query(populate_observations, tuple(row[1:]))

