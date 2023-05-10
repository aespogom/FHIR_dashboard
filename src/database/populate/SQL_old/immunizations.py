'''
    This module contains the logic to create and populate IMMUNIZATIONS SQL database table
    ATTENTION! Running this script will delete all existing tables and populate them with
    the our predefined data stored in data/synthea_output/csv.
    All changes will be lost.
'''

import database_connection
import pandas as pd
import numpy as np


## IMMUNIZATIONS
def populate_table(reset_table: bool):
    if reset_table:
        table_immunizations= '''
            IF OBJECT_ID('immunizations') IS NOT NULL
                DROP TABLE immunizations;  
            CREATE TABLE immunizations (
                DATE date,
                PATIENT UNIQUEIDENTIFIER not null,
                ENCOUNTER UNIQUEIDENTIFIER,
                CODE integer,
                DESCRIPTION nvarchar(150),
                BASE_COST integer,
                primary key (PATIENT, ENCOUNTER, DATE, CODE)
            );'''

        database_connection.execute_query(table_immunizations)

    data = pd.read_csv('./src/database/data/synthea_output/csv/immunizations.csv')   
    df = pd.DataFrame(data)
    df = df.replace(np.nan,'',regex = True)
    df['DATE']= pd.to_datetime(df['DATE'], errors='ignore')
    for row in df.itertuples():

        populate_immunizations = '''
            INSERT INTO immunizations 
            (DATE,PATIENT,ENCOUNTER,CODE,DESCRIPTION,BASE_COST)
            VALUES (?,?,?,?,?,?)
            '''
        database_connection.execute_query(populate_immunizations,tuple(row[1:]))


