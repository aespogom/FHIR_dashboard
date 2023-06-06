'''
    This module contains the logic to create and populate CLAIMS SQL database table
    ATTENTION! Running this script will delete all existing tables and populate them with
    the our predefined data stored in data/synthea_output/csv.
    All changes will be lost.
'''

import database_connection
import pandas as pd
import numpy as np


## CLAIMS
def populate_table(reset_table: bool):
    if reset_table:
        table_claims= '''
            IF OBJECT_ID('claims') IS NOT NULL
                DROP TABLE claims;  
            CREATE TABLE claims (
                ID UNIQUEIDENTIFIER,
                PATIENTID UNIQUEIDENTIFIER,
                PROVIDERID UNIQUEIDENTIFIER,
                PRIMARYPATIENTINSURANCEID UNIQUEIDENTIFIER,
                SECONDARYPATIENTINSURANCEID nvarchar(150),
                DEPARTMENTID integer,
                PATIENTDEPARTMENTID integer,
                DIAGNOSIS1 nvarchar(150),
                DIAGNOSIS2 nvarchar(150),
                DIAGNOSIS3 nvarchar(150),
                DIAGNOSIS4 nvarchar(150),
                DIAGNOSIS5 nvarchar(150),
                DIAGNOSIS6 nvarchar(150),
                DIAGNOSIS7 nvarchar(150),
                DIAGNOSIS8 nvarchar(150),
                REFERRINGPROVIDERID nvarchar(150),
                APPOINTMENTID UNIQUEIDENTIFIER,
                CURRENTILLNESSDATE date,
                SERVICEDATE date,
                SUPERVISINGPROVIDERID UNIQUEIDENTIFIER,
                STATUS1 nvarchar(150),
                STATUS2 nvarchar(150),
                STATUSP nvarchar(150),
                OUTSTANDING1 integer,
                OUTSTANDING2 integer,
                OUTSTANDINGP integer,
                LASTBILLEDDATE1 date,
                LASTBILLEDDATE2 date,
                LASTBILLEDDATEP date,
                HEALTHCARECLAIMTYPEID1 integer,
                HEALTHCARECLAIMTYPEID2 integer
                primary key (ID)
            );'''

        database_connection.execute_query(table_claims)

    data = pd.read_csv('./src/database/data/synthea_output/csv/claims.csv')   
    df = pd.DataFrame(data)
    df = df.reset_index(drop=True)
    df = df.replace(np.nan,'',regex = True)
    df['CURRENTILLNESSDATE']= pd.to_datetime(df['CURRENTILLNESSDATE'], errors='ignore')
    df['SERVICEDATE']= pd.to_datetime(df['SERVICEDATE'], errors='ignore')
    df['LASTBILLEDDATE1']= pd.to_datetime(df['LASTBILLEDDATE1'], errors='ignore')
    df['LASTBILLEDDATE2']= pd.to_datetime(df['LASTBILLEDDATE2'], errors='ignore')
    df['LASTBILLEDDATEP']= pd.to_datetime(df['LASTBILLEDDATEP'], errors='ignore')
    
    for row in df.itertuples():
        populate_claims = '''
            INSERT INTO claims 
            (ID,PATIENTID,PROVIDERID,PRIMARYPATIENTINSURANCEID,SECONDARYPATIENTINSURANCEID,DEPARTMENTID,PATIENTDEPARTMENTID,DIAGNOSIS1,DIAGNOSIS2,DIAGNOSIS3,DIAGNOSIS4,DIAGNOSIS5,DIAGNOSIS6,DIAGNOSIS7,DIAGNOSIS8,REFERRINGPROVIDERID,APPOINTMENTID,CURRENTILLNESSDATE,SERVICEDATE,SUPERVISINGPROVIDERID,STATUS1,STATUS2,STATUSP,OUTSTANDING1,OUTSTANDING2,OUTSTANDINGP,LASTBILLEDDATE1,LASTBILLEDDATE2,LASTBILLEDDATEP,HEALTHCARECLAIMTYPEID1,HEALTHCARECLAIMTYPEID2)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            '''
        database_connection.execute_query(populate_claims,tuple(row[1:]))

