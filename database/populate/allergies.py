'''
    This module contains the logic to create and populate ALLERGIES SQL database table
    ATTENTION! Running this script will delete all existing tables and populate them with
    the our predefined data stored in data/synthea_output/csv.
    All changes will be lost.
'''

import database_connection
import pandas as pd
import numpy as np


## ALLERGIES ##
table_allergies = '''
    IF OBJECT_ID('allergies') IS NOT NULL
        DROP TABLE allergies;  
    CREATE TABLE allergies (
        START date,
        STOP date,
        PATIENT UNIQUEIDENTIFIER not null,
        ENCOUNTER UNIQUEIDENTIFIER,
        CODE integer,
        SYSTEM nvarchar(150),
        DESCRIPTION nvarchar(150),
        TYPE nvarchar(150),
        CATEGORY nvarchar(150),
        REACTION1 nvarchar(150),
        DESCRIPTION1 nvarchar(150),
        SEVERITY1 nvarchar(150),
        REACTION2 nvarchar(150),
        DESCRIPTION2 nvarchar(150),
        SEVERITY2 nvarchar(150)
        primary key (PATIENT, ENCOUNTER, START, CODE)
    );'''

database_connection.execute_query(table_allergies)

data = pd.read_csv('./database/data/synthea_output/csv/allergies.csv')   
df = pd.DataFrame(data)
df = df.replace(np.nan,'',regex = True)
df['START']= pd.to_datetime(df['START'], errors='ignore')
df['STOP']= pd.to_datetime(df['STOP'], errors='ignore')
df['SYSTEM'] = df['SYSTEM'].replace('-',' ',regex = True)

for row in df.itertuples():
    populate_allergies = '''
        INSERT INTO allergies 
        (START, STOP, PATIENT,ENCOUNTER,CODE,SYSTEM,DESCRIPTION,TYPE,CATEGORY,REACTION1,DESCRIPTION1,SEVERITY1,REACTION2,DESCRIPTION2,SEVERITY2)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        '''
    database_connection.execute_query(populate_allergies, tuple(row[1:]))
