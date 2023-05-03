'''
    This module contains the logic to create and populate PATIENTS SQL database table
    ATTENTION! Running this script will delete all existing tables and populate them with
    the our predefined data stored in data/synthea_output/csv.
    All changes will be lost.
'''

import database_connection
import pandas as pd
import numpy as np


## PATIENTS
def populate_table(reset_table: bool):
    if reset_table:
        table_patients= '''
            IF OBJECT_ID('patients') IS NOT NULL
                DROP TABLE patients;  
            CREATE TABLE patients (
                ID UNIQUEIDENTIFIER not null,
                BIRTHDATE date,
                DEATHDATE date,
                SSN nvarchar(150),
                DRIVERS nvarchar(150),
                PASSPORT nvarchar(150),
                PREFIX nvarchar(150),
                FIRST nvarchar(150),
                LAST nvarchar(150),
                SUFFIX nvarchar(150),
                MAIDEN nvarchar(150),
                MARITAL nvarchar(150),
                RACE nvarchar(150),
                ETHNICITY nvarchar(150),
                GENDER nvarchar(150),
                BIRTHPLACE nvarchar(150),
                ADDRESS nvarchar(150),
                CITY nvarchar(150),
                STATE nvarchar(150),
                COUNTY nvarchar(150),
                FIPS nvarchar(150),
                ZIP integer,
                LAT integer,
                LON integer,
                HEALTHCARE_EXPENSES integer,
                HEALTHCARE_COVERAGE integer,
                INCOME integer,
                primary key (ID)
            );'''

        database_connection.execute_query(table_patients)

    data = pd.read_csv('./database/data/synthea_output/csv/patients.csv')   
    df = pd.DataFrame(data)
    df = df.reset_index(drop=True)
    df = df.replace(np.nan,'',regex = True)
    df['BIRTHDATE']= pd.to_datetime(df['BIRTHDATE'], errors='ignore')
    df['DEATHDATE']= pd.to_datetime(df['DEATHDATE'], errors='ignore')

    populate_patients = '''
        INSERT INTO patients 
        (ID,BIRTHDATE,DEATHDATE,SSN,DRIVERS,PASSPORT,PREFIX,FIRST,LAST,SUFFIX,MAIDEN,MARITAL,RACE,ETHNICITY,GENDER,BIRTHPLACE,ADDRESS,CITY,STATE,COUNTY,FIPS,ZIP,LAT,LON,HEALTHCARE_EXPENSES,HEALTHCARE_COVERAGE,INCOME)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        '''
    database_connection.fast_insertion_dataframe(populate_patients, df)

