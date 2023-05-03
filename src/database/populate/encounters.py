'''
    This module contains the logic to create and populate ENCOUNTERS SQL database table
    ATTENTION! Running this script will delete all existing tables and populate them with
    the our predefined data stored in data/synthea_output/csv.
    All changes will be lost.
'''

import database_connection
import pandas as pd
import numpy as np


## ENCOUNTERS
def populate_table(reset_table: bool):
    if reset_table:
        table_encounters= '''
            IF OBJECT_ID('encounters') IS NOT NULL
                DROP TABLE encounters;  
            CREATE TABLE encounters (
                ID UNIQUEIDENTIFIER,
                ORGANIZATION UNIQUEIDENTIFIER,
                PROVIDER UNIQUEIDENTIFIER,
                PAYER UNIQUEIDENTIFIER,
                ENCOUNTERCLASS nvarchar(150),
                CODE integer,
                DESCRIPTION nvarchar(150),
                BASE_ENCOUNTER_COST integer,
                TOTAL_CLAIM_COST integer,
                PAYER_COVERAGE integer,
                REASONCODE integer,
                REASONDESCRIPTION nvarchar(150),
                START date,
                STOP date,
                PATIENT UNIQUEIDENTIFIER not null,
                primary key (ID)
            );'''

        database_connection.execute_query(table_encounters)

    data = pd.read_csv('./database/data/synthea_output/csv/encounters.csv')   
    df = pd.DataFrame(data)
    df = df.reset_index(drop=True)
    df = df.replace(np.nan,'',regex = True)
    df['START']= pd.to_datetime(df['START'], errors='ignore')
    df['STOP']= pd.to_datetime(df['STOP'], errors='ignore')

    populate_encounters = '''
        INSERT INTO encounters 
        (ID,START,STOP,PATIENT,ORGANIZATION,PROVIDER,PAYER,ENCOUNTERCLASS,CODE,DESCRIPTION,BASE_ENCOUNTER_COST,TOTAL_CLAIM_COST,PAYER_COVERAGE,REASONCODE,REASONDESCRIPTION)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        '''
    database_connection.fast_insertion_dataframe(populate_encounters, df)
