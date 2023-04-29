'''
    This module contains the logic to create and populate the SQL database
    ATTENTION! Running this script will delete all existing tables and populate them with
    the our predefined data stored in data/synthea_output/csv.
    All changes will be lost.
'''

import database_connection
import pandas as pd
import numpy as np


# ## ALLERGIES ##
# table_allergies = '''
#     IF OBJECT_ID('allergies') IS NOT NULL
#         DROP TABLE allergies;  
#     CREATE TABLE allergies (
#         START date,
#         STOP date,
#         PATIENT UNIQUEIDENTIFIER not null,
#         ENCOUNTER UNIQUEIDENTIFIER,
#         CODE integer,
#         SYSTEM nvarchar(150),
#         DESCRIPTION nvarchar(150),
#         TYPE nvarchar(150),
#         CATEGORY nvarchar(150),
#         REACTION1 nvarchar(150),
#         DESCRIPTION1 nvarchar(150),
#         SEVERITY1 nvarchar(150),
#         REACTION2 nvarchar(150),
#         DESCRIPTION2 nvarchar(150),
#         SEVERITY2 nvarchar(150)
#         primary key (PATIENT, ENCOUNTER, START, CODE)
#     );'''

# database_connection.execute_query(table_allergies)

# data = pd.read_csv('./database/data/synthea_output/csv/allergies.csv')   
# df = pd.DataFrame(data)
# df = df.replace(np.nan,'',regex = True)
# df['START']= pd.to_datetime(df['START'], errors='ignore')
# df['STOP']= pd.to_datetime(df['STOP'], errors='ignore')
# df['SYSTEM'] = df['SYSTEM'].replace('-',' ',regex = True)

# for row in df.itertuples():
#     populate_allergies = '''
#         INSERT INTO allergies 
#         (START, STOP, PATIENT,ENCOUNTER,CODE,SYSTEM,DESCRIPTION,TYPE,CATEGORY,REACTION1,DESCRIPTION1,SEVERITY1,REACTION2,DESCRIPTION2,SEVERITY2)
#         VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
#         '''
#     database_connection.execute_query(populate_allergies, tuple(row[1:]))

# ## CAREPLANS
# table_careplans = '''
#     IF OBJECT_ID('careplans') IS NOT NULL
#         DROP TABLE careplans;  
#     CREATE TABLE careplans (
#         START date,
#         STOP date,
#         PATIENT UNIQUEIDENTIFIER not null,
#         ENCOUNTER UNIQUEIDENTIFIER,
#         CODE integer,
#         DESCRIPTION nvarchar(150),
#         REASONCODE integer,
#         REASONDESCRIPTION nvarchar(150)
#         primary key (PATIENT, ENCOUNTER, START, CODE)
#     );'''

# database_connection.execute_query(table_careplans)

# data = pd.read_csv('./database/data/synthea_output/csv/careplans.csv')   
# df = pd.DataFrame(data)
# df = df.replace(np.nan,'',regex = True)
# df['START']= pd.to_datetime(df['START'], errors='ignore')
# df['STOP']= pd.to_datetime(df['STOP'], errors='ignore')

# for row in df.itertuples():
#     populate_careplans = '''
#         INSERT INTO careplans 
#         (START,STOP,PATIENT,ENCOUNTER,CODE,DESCRIPTION,REASONCODE,REASONDESCRIPTION)
#         VALUES (?,?,?,?,?,?,?,?)
#         '''
#     database_connection.execute_query(populate_careplans, tuple(row[2:]))

# ## CLAIMS_TRANSACTIONS
# table_claims_transactions = '''
#     IF OBJECT_ID('claims_transactions') IS NOT NULL
#         DROP TABLE claims_transactions;  
#     CREATE TABLE claims_transactions (
#         ID UNIQUEIDENTIFIER,
#         CLAIMID UNIQUEIDENTIFIER,
#         CHARGEID integer,
#         PATIENTID UNIQUEIDENTIFIER,
#         TYPE nvarchar(150),
#         AMOUNT integer,
#         METHOD nvarchar(150),
#         FROMDATE date,
#         TODATE date,
#         PLACEOFSERVICE UNIQUEIDENTIFIER,
#         PROCEDURECODE integer,
#         MODIFIER1 nvarchar(150),
#         MODIFIER2 nvarchar(150),
#         DIAGNOSISREF1 nvarchar(150),
#         DIAGNOSISREF2 nvarchar(150),
#         DIAGNOSISREF3 nvarchar(150),
#         DIAGNOSISREF4 nvarchar(150),
#         UNITS integer,
#         DEPARTMENTID integer,
#         NOTES nvarchar(150),
#         UNITAMOUNT integer,
#         TRANSFEROUTID nvarchar(150),
#         TRANSFERTYPE nvarchar(150),
#         PAYMENTS integer,
#         ADJUSTMENTS integer,
#         TRANSFERS nvarchar(150),
#         OUTSTANDING integer,
#         APPOINTMENTID UNIQUEIDENTIFIER,
#         LINENOTE nvarchar(150),
#         PATIENTINSURANCEID UNIQUEIDENTIFIER,
#         FEESCHEDULEID integer,
#         PROVIDERID UNIQUEIDENTIFIER,
#         SUPERVISINGPROVIDERID UNIQUEIDENTIFIER
#         primary key (ID)
#     );'''

# # database_connection.execute_query(table_claims_transactions)

# data = pd.read_csv('./database/data/synthea_output/csv/claims_transactions.csv')   
# df = pd.DataFrame(data)
# df = df.replace(np.nan,'',regex = True)
# df['FROMDATE']= pd.to_datetime(df['FROMDATE'], errors='ignore')
# df['TODATE']= pd.to_datetime(df['TODATE'], errors='ignore')

# for row in df.itertuples():
#     populate_claims_transactions = '''
#         INSERT INTO claims_transactions 
#         (ID,CLAIMID,CHARGEID,PATIENTID,TYPE,AMOUNT,METHOD,FROMDATE,TODATE,PLACEOFSERVICE,PROCEDURECODE,MODIFIER1,MODIFIER2,DIAGNOSISREF1,DIAGNOSISREF2,DIAGNOSISREF3,DIAGNOSISREF4,UNITS,DEPARTMENTID,NOTES,UNITAMOUNT,TRANSFEROUTID,TRANSFERTYPE,PAYMENTS,ADJUSTMENTS,TRANSFERS,OUTSTANDING,APPOINTMENTID,LINENOTE,PATIENTINSURANCEID,FEESCHEDULEID,PROVIDERID,SUPERVISINGPROVIDERID)
#         VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
#         '''
#     database_connection.execute_query(populate_claims_transactions, tuple(row[1:]))


## CLAIMS
table_claims= '''
    IF OBJECT_ID('claims') IS NOT NULL
        DROP TABLE claims;  
    CREATE TABLE claims (
        ID UNIQUEIDENTIFIER,
        PATIENTID UNIQUEIDENTIFIER,
        PROVIDERID UNIQUEIDENTIFIER,
        PRIMARYPATIENTINSURANCEID UNIQUEIDENTIFIER,
        SECONDARYPATIENTINSURANCEID UNIQUEIDENTIFIER,
        DEPARTMENTID integer,
        PATIENTDEPARTMENTID UNIQUEIDENTIFIER,
        DIAGNOSIS1 nvarchar(150),
        DIAGNOSIS2 nvarchar(150),
        DIAGNOSIS3 nvarchar(150),
        DIAGNOSIS4 nvarchar(150),
        DIAGNOSIS5 nvarchar(150),
        DIAGNOSIS6 nvarchar(150),
        DIAGNOSIS7 nvarchar(150),
        DIAGNOSIS8 nvarchar(150),
        REFERRINGPROVIDERID UNIQUEIDENTIFIER,
        APPOINTMENTID UNIQUEIDENTIFIER,
        CURRENTILLNESSDATE date,
        SERVICEDATE date,
        SUPERVISINGPROVIDERID UNIQUEIDENTIFIER,
        STATUS1 nvarchar(150),
        STATUS2 nvarchar(150),
        STATUSP nvarchar(150),
        OUTSTANDING1 nvarchar(150),
        OUTSTANDING2 nvarchar(150),
        OUTSTANDINGP nvarchar(150),
        LASTBILLEDDATE1 date,
        LASTBILLEDDATE2 date,
        LASTBILLEDDATEP date,
        HEALTHCARECLAIMTYPEID1 UNIQUEIDENTIFIER,
        HEALTHCARECLAIMTYPEID2 UNIQUEIDENTIFIER
        primary key (ID)
    );'''

# database_connection.execute_query(table_claims)

data = pd.read_csv('./database/data/synthea_output/csv/claims.csv')   
df = pd.DataFrame(data)
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
    database_connection.execute_query(populate_claims, tuple(row[1:]))


## CONDITIONS
table_conditions= '''
    IF OBJECT_ID('conditions') IS NOT NULL
        DROP TABLE conditions;  
    CREATE TABLE conditions (
        START date,
        STOP date,
        PATIENT UNIQUEIDENTIFIER not null,
        ENCOUNTER UNIQUEIDENTIFIER,
        CODE integer,
        DESCRIPTION nvarchar(150),
        primary key (PATIENT, ENCOUNTER, START, CODE)
    );'''

# database_connection.execute_query(table_conditions)

data = pd.read_csv('./database/data/synthea_output/csv/conditions.csv')   
df = pd.DataFrame(data)
df = df.replace(np.nan,'',regex = True)
df['START']= pd.to_datetime(df['START'], errors='ignore')
df['STOP']= pd.to_datetime(df['STOP'], errors='ignore')

for row in df.itertuples():
    populate_conditions = '''
        INSERT INTO conditions 
        (START,STOP,PATIENT,ENCOUNTER,CODE,DESCRIPTION)
        VALUES (?,?,?,?,?,?)
        '''
    database_connection.execute_query(populate_conditions, tuple(row[1:]))


## DEVICES
table_devices= '''
    IF OBJECT_ID('devices') IS NOT NULL
        DROP TABLE devices;  
    CREATE TABLE devices (
        START date,
        STOP date,
        PATIENT UNIQUEIDENTIFIER not null,
        ENCOUNTER UNIQUEIDENTIFIER,
        CODE integer,
        DESCRIPTION nvarchar(150),
        UDI UNIQUEIDENTIFIER,
        primary key (PATIENT, ENCOUNTER, START, CODE)
    );'''

# database_connection.execute_query(table_devices)

data = pd.read_csv('./database/data/synthea_output/csv/devices.csv')   
df = pd.DataFrame(data)
df = df.replace(np.nan,'',regex = True)
df['START']= pd.to_datetime(df['START'], errors='ignore')
df['STOP']= pd.to_datetime(df['STOP'], errors='ignore')

for row in df.itertuples():
    populate_devices = '''
        INSERT INTO devices 
        (START,STOP,PATIENT,ENCOUNTER,CODE,DESCRIPTION,UDI)
        VALUES (?,?,?,?,?,?,?)
        '''
    database_connection.execute_query(populate_devices, tuple(row[1:]))

## ENCOUNTERS
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

# database_connection.execute_query(table_encounters)

data = pd.read_csv('./database/data/synthea_output/csv/encounters.csv')   
df = pd.DataFrame(data)
df = df.replace(np.nan,'',regex = True)
df['START']= pd.to_datetime(df['START'], errors='ignore')
df['STOP']= pd.to_datetime(df['STOP'], errors='ignore')

for row in df.itertuples():
    populate_encounters = '''
        INSERT INTO encounters 
        (ID,START,STOP,PATIENT,ORGANIZATION,PROVIDER,PAYER,ENCOUNTERCLASS,CODE,DESCRIPTION,BASE_ENCOUNTER_COST,TOTAL_CLAIM_COST,PAYER_COVERAGE,REASONCODE,REASONDESCRIPTION)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        '''
    database_connection.execute_query(populate_encounters, tuple(row[1:]))


## IMAGING STUDIES
table_imaging_studies= '''
    IF OBJECT_ID('imaging_studies') IS NOT NULL
        DROP TABLE imaging_studies;  
    CREATE TABLE imaging_studies (
        ID UNIQUEIDENTIFIER,
        DATE date,
        PATIENT UNIQUEIDENTIFIER not null,
        ENCOUNTER UNIQUEIDENTIFIER,
        SERIES_UID UNIQUEIDENTIFIER,
        BODYSITE_CODE integer,
        BODYSITE_DESCRIPTION nvarchar(150),
        MODALITY_CODE integer,
        MODALITY_DESCRIPTION nvarchar(150),
        INSTANCE_UID UNIQUEIDENTIFIER,
        SOP_CODE integer,
        SOP_DESCRIPTION nvarchar(150),
        PROCEDURE_CODE integer,
        primary key (ID)
    );'''

# database_connection.execute_query(table_imaging_studies)

data = pd.read_csv('./database/data/synthea_output/csv/imaging_studies.csv')   
df = pd.DataFrame(data)
df = df.replace(np.nan,'',regex = True)
df['DATE']= pd.to_datetime(df['DATE'], errors='ignore')

for row in df.itertuples():
    populate_imaging_studies = '''
        INSERT INTO imaging_studies 
        (ID,DATE,PATIENT,ENCOUNTER,SERIES_UID,BODYSITE_CODE,BODYSITE_DESCRIPTION,MODALITY_CODE,MODALITY_DESCRIPTION,INSTANCE_UID,SOP_CODE,SOP_DESCRIPTION,PROCEDURE_CODE)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        '''
    database_connection.execute_query(populate_imaging_studies, tuple(row[1:]))


## IMMUNIZATIONS
table_immunizations= '''
    IF OBJECT_ID('immunizations') IS NOT NULL
        DROP TABLE immunizations;  
    CREATE TABLE immunizations (
        DATE date,
        PATIENT UNIQUEIDENTIFIER not null,
        ENCOUNTER UNIQUEIDENTIFIER,
        CODE integer,
        DESCRIPTION nvarchar(150),
        BASE_COST integer,
        primary key (PATIENT, ENCOUNTER, DATE, CODE)
    );'''

# database_connection.execute_query(table_immunizations)

data = pd.read_csv('./database/data/synthea_output/csv/immunizations.csv')   
df = pd.DataFrame(data)
df = df.replace(np.nan,'',regex = True)
df['DATE']= pd.to_datetime(df['DATE'], errors='ignore')

for row in df.itertuples():
    populate_immunizations = '''
        INSERT INTO immunizations 
        (DATE,PATIENT,ENCOUNTER,CODE,DESCRIPTION,BASE_COST)
        VALUES (?,?,?,?,?,?)
        '''
    database_connection.execute_query(populate_immunizations, tuple(row[1:]))



## MEDICATIONS
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
        DISPENSES nvarchar(150),
        TOTALCOST integer,
        REASONCODE integer,
        REASONDESCRIPTION nvarchar(150),
        primary key (PATIENT, ENCOUNTER, START, CODE)
    );'''

# database_connection.execute_query(table_medications)

data = pd.read_csv('./database/data/synthea_output/csv/medications.csv')   
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


## OBSERVATIONS
table_observations= '''
    IF OBJECT_ID('observations') IS NOT NULL
        DROP TABLE observations;  
    CREATE TABLE observations (
        DATE date,
        PATIENT UNIQUEIDENTIFIER not null,
        ENCOUNTER UNIQUEIDENTIFIER,
        CATEGORY nvarchar(150),
        CODE integer,
        DESCRIPTION nvarchar(150),
        VALUE integer,
        UNITS nvarchar(150),
        TYPE nvarchar(150),
        primary key (PATIENT, ENCOUNTER, DATE, CODE)
    );'''

# database_connection.execute_query(table_observations)

data = pd.read_csv('./database/data/synthea_output/csv/observations.csv')   
df = pd.DataFrame(data)
df = df.replace(np.nan,'',regex = True)
df['DATE']= pd.to_datetime(df['DATE'], errors='ignore')

for row in df.itertuples():
    populate_observations = '''
        INSERT INTO observations 
        (DATE,PATIENT,ENCOUNTER,CATEGORY,CODE,DESCRIPTION,VALUE,UNITS,TYPE)
        VALUES (?,?,?,?,?,?,?,?,?)
        '''
    database_connection.execute_query(populate_observations, tuple(row[1:]))

