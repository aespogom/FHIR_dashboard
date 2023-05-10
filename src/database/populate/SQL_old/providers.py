'''
    This module contains the logic to create and populate PROVIDERS SQL database table
    ATTENTION! Running this script will delete all existing tables and populate them with
    the our predefined data stored in data/synthea_output/csv.
    All changes will be lost.
'''

import database_connection
import pandas as pd
import numpy as np


## PROVIDERS
def populate_table(reset_table: bool):
    if reset_table:
        table_providers= '''
            IF OBJECT_ID('providers') IS NOT NULL
                DROP TABLE providers;  
            CREATE TABLE providers (
                ID UNIQUEIDENTIFIER,
                ORGANIZATION nvarchar(150),
                NAME nvarchar(150),
                GENDER nvarchar(150),
                SPECIALTY nvarchar(150),
                ADDRESS nvarchar(150),
                CITY nvarchar(150),
                STATE nvarchar(150),
                ZIP integer,
                LAT integer,
                LON integer,
                ENCOUNTERS integer,
                PROCEDURES integer,
                primary key (ID)
            );'''

        database_connection.execute_query(table_providers)

    data = pd.read_csv('./src/database/data/synthea_output/csv/providers.csv')   
    df = pd.DataFrame(data)
    df = df.replace(np.nan,'',regex = True)
    for row in df.itertuples():

        populate_providers = '''
            INSERT INTO providers 
            (ID,ORGANIZATION,NAME,GENDER,SPECIALTY,ADDRESS,CITY,STATE,ZIP,LAT,LON,ENCOUNTERS,PROCEDURES)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            '''
        database_connection.execute_query(populate_providers, tuple(row[1:]))

