'''
    This module contains the logic to create and populate MEDICATIONS SQL database table
    ATTENTION! Running this script will delete all existing tables and populate them with
    the our predefined data stored in data/synthea_output/csv.
    All changes will be lost.
'''

import database_connection
import pandas as pd
import numpy as np


## MEDICATIONS
def populate_table(reset_table: bool):
    if reset_table:
        table_medications= '''
            IF OBJECT_ID('medications') IS NOT NULL
                DROP TABLE medications;  
            CREATE TABLE medications (
                START date,
                STOP date,
                PATIENT UNIQUEIDENTIFIER not null,
                PAYER UNIQUEIDENTIFIER,
                ENCOUNTER UNIQUEIDENTIFIER,
                CODE integer,
                DESCRIPTION nvarchar(150),
                BASE_COST integer,
                PAYER_COVERAGE integer,
                DISPENSES integer,
                TOTALCOST integer,
                REASONCODE integer,
                REASONDESCRIPTION nvarchar(150),
                primary key (PATIENT, ENCOUNTER, START, CODE)
            );'''

        database_connection.execute_query(table_medications)

    data = pd.read_csv('./src/database/data/synthea_output/csv/medications.csv')   
    df = pd.DataFrame(data)
    df = df.replace(np.nan,'',regex = True)
    df['START']= pd.to_datetime(df['START'], errors='ignore')
    df['STOP']= pd.to_datetime(df['STOP'], errors='ignore')
    for row in df.itertuples():

        populate_medications = '''
            INSERT INTO medications 
            (START,STOP,PATIENT,PAYER,ENCOUNTER,CODE,DESCRIPTION,BASE_COST,PAYER_COVERAGE,DISPENSES,TOTALCOST,REASONCODE,REASONDESCRIPTION)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            '''
        database_connection.execute_query(populate_medications, tuple(row[1:]))

