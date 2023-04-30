'''
    This module contains the logic to create and populate PAYERS SQL database table
    ATTENTION! Running this script will delete all existing tables and populate them with
    the our predefined data stored in data/synthea_output/csv.
    All changes will be lost.
'''

import database_connection
import pandas as pd
import numpy as np


## PAYERS
table_payers= '''
    IF OBJECT_ID('payers') IS NOT NULL
        DROP TABLE payers;  
    CREATE TABLE payers (
        ID UNIQUEIDENTIFIER not null,
        NAME nvarchar(150),
        OWNERSHIP nvarchar(150),
        ADDRESS nvarchar(150),
        CITY nvarchar(150),
        STATE_HEADQUARTERED nvarchar(150),
        ZIP integer,
        PHONE bigint,
        AMOUNT_COVERED integer,
        AMOUNT_UNCOVERED integer,
        REVENUE integer,
        COVERED_ENCOUNTERS integer,
        UNCOVERED_ENCOUNTERS integer,
        COVERED_MEDICATIONS integer,
        UNCOVERED_MEDICATIONS integer,
        COVERED_PROCEDURES integer,
        UNCOVERED_PROCEDURES integer,
        COVERED_IMMUNIZATIONS integer,
        UNCOVERED_IMMUNIZATIONS integer,
        UNIQUE_CUSTOMERS integer,
        QOLS_AVG integer,
        MEMBER_MONTHS integer,
        primary key (ID)
    );'''

database_connection.execute_query(table_payers)

data = pd.read_csv('./database/data/synthea_output/csv/payers.csv')   
df = pd.DataFrame(data)
df = df.replace(np.nan,'',regex = True)

for row in df.itertuples():
    populate_payers = '''
        INSERT INTO payers 
        (ID,NAME,OWNERSHIP,ADDRESS,CITY,STATE_HEADQUARTERED,ZIP,PHONE,AMOUNT_COVERED,AMOUNT_UNCOVERED,REVENUE,COVERED_ENCOUNTERS,UNCOVERED_ENCOUNTERS,COVERED_MEDICATIONS,UNCOVERED_MEDICATIONS,COVERED_PROCEDURES,UNCOVERED_PROCEDURES,COVERED_IMMUNIZATIONS,UNCOVERED_IMMUNIZATIONS,UNIQUE_CUSTOMERS,QOLS_AVG,MEMBER_MONTHS)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        '''
    database_connection.execute_query(populate_payers, tuple(row[1:]))

