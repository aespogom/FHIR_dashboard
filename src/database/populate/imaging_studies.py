'''
    This module contains the logic to create and populate IMAGING STUDIES SQL database table
    ATTENTION! Running this script will delete all existing tables and populate them with
    the our predefined data stored in data/synthea_output/csv.
    All changes will be lost.
'''

import database_connection
import pandas as pd
import numpy as np


## IMAGING STUDIES
def populate_table(reset_table: bool):
    if reset_table:
        table_imaging_studies= '''
            IF OBJECT_ID('imaging_studies') IS NOT NULL
                DROP TABLE imaging_studies;  
            CREATE TABLE imaging_studies (
                ID UNIQUEIDENTIFIER,
                DATE date,
                PATIENT UNIQUEIDENTIFIER not null,
                ENCOUNTER UNIQUEIDENTIFIER,
                SERIES_UID nvarchar(150),
                BODYSITE_CODE integer,
                BODYSITE_DESCRIPTION nvarchar(150),
                MODALITY_CODE nvarchar(150),
                MODALITY_DESCRIPTION nvarchar(150),
                INSTANCE_UID nvarchar(150),
                SOP_CODE nvarchar(150),
                SOP_DESCRIPTION nvarchar(150),
                PROCEDURE_CODE integer,
                primary key (ID)
            );'''

        database_connection.execute_query(table_imaging_studies)

    data = pd.read_csv('./src/database/data/synthea_output/csv/imaging_studies.csv')   
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

