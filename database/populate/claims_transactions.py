'''
    This module contains the logic to create and populate CLAIMS TRANSACTIONS SQL database table
    ATTENTION! Running this script will delete all existing tables and populate them with
    the our predefined data stored in data/synthea_output/csv.
    All changes will be lost.
'''

import database_connection
import pandas as pd
import numpy as np


## CLAIMS_TRANSACTIONS
table_claims_transactions = '''
    IF OBJECT_ID('claims_transactions') IS NOT NULL
        DROP TABLE claims_transactions;  
    CREATE TABLE claims_transactions (
        ID UNIQUEIDENTIFIER,
        CLAIMID UNIQUEIDENTIFIER,
        CHARGEID integer,
        PATIENTID UNIQUEIDENTIFIER,
        TYPE nvarchar(150),
        AMOUNT integer,
        METHOD nvarchar(150),
        FROMDATE date,
        TODATE date,
        PLACEOFSERVICE UNIQUEIDENTIFIER,
        PROCEDURECODE integer,
        MODIFIER1 nvarchar(150),
        MODIFIER2 nvarchar(150),
        DIAGNOSISREF1 nvarchar(150),
        DIAGNOSISREF2 nvarchar(150),
        DIAGNOSISREF3 nvarchar(150),
        DIAGNOSISREF4 nvarchar(150),
        UNITS integer,
        DEPARTMENTID integer,
        NOTES nvarchar(150),
        UNITAMOUNT integer,
        TRANSFEROUTID nvarchar(150),
        TRANSFERTYPE nvarchar(150),
        PAYMENTS integer,
        ADJUSTMENTS integer,
        TRANSFERS nvarchar(150),
        OUTSTANDING integer,
        APPOINTMENTID UNIQUEIDENTIFIER,
        LINENOTE nvarchar(150),
        PATIENTINSURANCEID UNIQUEIDENTIFIER,
        FEESCHEDULEID integer,
        PROVIDERID UNIQUEIDENTIFIER,
        SUPERVISINGPROVIDERID UNIQUEIDENTIFIER
        primary key (ID)
    );'''

# database_connection.execute_query(table_claims_transactions)

data = pd.read_csv('./database/data/synthea_output/csv/claims_transactions.csv')   
df = pd.DataFrame(data)
df = df.replace(np.nan,'',regex = True)
df['FROMDATE']= pd.to_datetime(df['FROMDATE'], errors='ignore')
df['TODATE']= pd.to_datetime(df['TODATE'], errors='ignore')

for row in df.itertuples():
    populate_claims_transactions = '''
        INSERT INTO claims_transactions 
        (ID,CLAIMID,CHARGEID,PATIENTID,TYPE,AMOUNT,METHOD,FROMDATE,TODATE,PLACEOFSERVICE,PROCEDURECODE,MODIFIER1,MODIFIER2,DIAGNOSISREF1,DIAGNOSISREF2,DIAGNOSISREF3,DIAGNOSISREF4,UNITS,DEPARTMENTID,NOTES,UNITAMOUNT,TRANSFEROUTID,TRANSFERTYPE,PAYMENTS,ADJUSTMENTS,TRANSFERS,OUTSTANDING,APPOINTMENTID,LINENOTE,PATIENTINSURANCEID,FEESCHEDULEID,PROVIDERID,SUPERVISINGPROVIDERID)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        '''
    database_connection.execute_query(populate_claims_transactions, tuple(row[1:]))
