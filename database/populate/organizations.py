'''
    This module contains the logic to create and populate ORGANIZATIONS SQL database table
    ATTENTION! Running this script will delete all existing tables and populate them with
    the our predefined data stored in data/synthea_output/csv.
    All changes will be lost.
'''

import database_connection
import pandas as pd
import numpy as np


## ORGANIZATIONS
table_organizations= '''
    IF OBJECT_ID('organizations') IS NOT NULL
        DROP TABLE organizations;  
    CREATE TABLE organizations (
        ID UNIQUEIDENTIFIER,
        NAME nvarchar(150),
        ADDRESS nvarchar(150),
        CITY nvarchar(150),
        STATE nvarchar(150),
        ZIP integer,
        LAT integer,
        LON integer,
        PHONE bigint,
        REVENUE integer,
        UTILIZATION integer,
        primary key (ID)
    );'''

database_connection.execute_query(table_organizations)

data = pd.read_csv('./database/data/synthea_output/csv/organizations.csv')   
df = pd.DataFrame(data)
df = df.replace(np.nan,'',regex = True)

for row in df.itertuples():
    populate_organizations = '''
        INSERT INTO organizations 
        (ID,NAME,ADDRESS,CITY,STATE,ZIP,LAT,LON,PHONE,REVENUE,UTILIZATION)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
        '''
    database_connection.execute_query(populate_organizations, tuple(row[1:]))

