'''
    This module contains the logic to create and populate SUPPLIES SQL database table
    ATTENTION! Running this script will delete all existing tables and populate them with
    the our predefined data stored in data/synthea_output/csv.
    All changes will be lost.
'''

import database_connection
import pandas as pd
import numpy as np


## SUPPLIES
def populate_table(reset_table: bool):
    if reset_table:
        table_supplies= '''
            IF OBJECT_ID('supplies') IS NOT NULL
                DROP TABLE supplies;  
            CREATE TABLE supplies (
                DATE date,
                PATIENT UNIQUEIDENTIFIER not null,
                ENCOUNTER UNIQUEIDENTIFIER,
                CODE integer,
                DESCRIPTION nvarchar(150),
                QUANTITY integer,
                primary key (PATIENT, ENCOUNTER, DATE, CODE)
            );'''

        database_connection.execute_query(table_supplies)

    data = pd.read_csv('./database/data/synthea_output/csv/supplies.csv')   
    df = pd.DataFrame(data)
    df = df.reset_index(drop=True)
    df = df.replace(np.nan,'',regex = True)

    populate_supplies = '''
        INSERT INTO supplies 
        (DATE,PATIENT,ENCOUNTER,CODE,DESCRIPTION,QUANTITY)
        VALUES (?,?,?,?,?,?)
        '''
    database_connection.fast_insertion_dataframe(populate_supplies, df)

