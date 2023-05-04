'''
    This module contains the logic to create and populate PROCEDURES SQL database table
    ATTENTION! Running this script will delete all existing tables and populate them with
    the our predefined data stored in data/synthea_output/csv.
    All changes will be lost.
'''

import database_connection
import pandas as pd
import numpy as np


## PROCEDURES
def populate_table(reset_table: bool):
    if reset_table:
        table_procedures= '''
            IF OBJECT_ID('procedures') IS NOT NULL
                DROP TABLE procedures;  
            CREATE TABLE procedures (
                START date,
                STOP date,
                PATIENT UNIQUEIDENTIFIER not null,
                ENCOUNTER UNIQUEIDENTIFIER,
                CODE integer,
                DESCRIPTION nvarchar(150),
                BASE_COST integer,
                REASONCODE integer,
                REASONDESCRIPTION nvarchar(150),
                primary key (PATIENT, ENCOUNTER, START, CODE)
            );'''

        database_connection.execute_query(table_procedures)

    data = pd.read_csv('./src/database/data/synthea_output/csv/procedures.csv')   
    df = pd.DataFrame(data)
    df = df.replace(np.nan,'',regex = True)
    df['START']= pd.to_datetime(df['START'], errors='ignore')
    df['STOP']= pd.to_datetime(df['STOP'], errors='ignore')
    for row in df.itertuples():

        populate_procedures = '''
            INSERT INTO procedures 
            (START,STOP,PATIENT,ENCOUNTER,CODE,DESCRIPTION,BASE_COST,REASONCODE,REASONDESCRIPTION)
            VALUES (?,?,?,?,?,?,?,?,?)
            '''
        database_connection.execute_query(populate_procedures,  tuple(row[1:]))

