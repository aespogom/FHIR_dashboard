'''
    This module contains the logic to create and populate PAYER TRANSITIONS SQL database table
    ATTENTION! Running this script will delete all existing tables and populate them with
    the our predefined data stored in data/synthea_output/csv.
    All changes will be lost.
'''

import database_connection
import pandas as pd
import numpy as np


## PAYER TRANSITIONS
def populate_table(reset_table: bool):
    if reset_table:
        table_payer_transitions= '''
            IF OBJECT_ID('payer_transitions') IS NOT NULL
                DROP TABLE payer_transitions;  
            CREATE TABLE payer_transitions (
                PATIENT UNIQUEIDENTIFIER not null,
                MEMBERID UNIQUEIDENTIFIER not null,
                START_DATE date,
                END_DATE date,
                PAYER UNIQUEIDENTIFIER not null,
                SECONDARY_PAYER nvarchar(150),
                PLAN_OWNERSHIP nvarchar(150),
                OWNER_NAME nvarchar(150),
                primary key (PATIENT, MEMBERID, START_DATE)
            );'''

        database_connection.execute_query(table_payer_transitions)

    data = pd.read_csv('./database/data/synthea_output/csv/payer_transitions.csv')   
    df = pd.DataFrame(data)
    df = df.reset_index(drop=True)
    df = df.replace(np.nan,'',regex = True)
    df['START_DATE']= pd.to_datetime(df['START_DATE'], errors='ignore')
    df['END_DATE']= pd.to_datetime(df['END_DATE'], errors='ignore')

    populate_payer_transitions = '''
        INSERT INTO payer_transitions 
        (PATIENT,MEMBERID,START_DATE,END_DATE,PAYER,SECONDARY_PAYER,PLAN_OWNERSHIP,OWNER_NAME)
        VALUES (?,?,?,?,?,?,?,?)
        '''
    database_connection.fast_insertion_dataframe(populate_payer_transitions, df)

