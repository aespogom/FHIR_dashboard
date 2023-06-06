'''
    This module contains all the available queries for the SQL database
    ATTENTION! Deprecated, do not use
'''

from datetime import datetime
from database.populate.SQL_old.database_connection import return_query
import constants as cte
from utils import list_by_table_name, filter_start_stop, get_by_encounter_patient_ID, get_by_ID

#Allergies
def list_allergies():
    return list_by_table_name(cte.TABLE_NAME_ALLERGIES)

def filter_allergies_by_datetime(start: datetime, stop: datetime):
    return filter_start_stop(cte.TABLE_NAME_ALLERGIES, start, stop)

def get_allergy_by_encounter_patient_ID(encounter_ID: str = None, patient_ID: str = None):
    return get_by_encounter_patient_ID(cte.TABLE_NAME_ALLERGIES, encounter_ID, patient_ID)

#Careplans
def list_careplans():
    return list_by_table_name(cte.TABLE_NAME_CAREPLANS)

def filter_careplans_by_datetime(start: datetime, stop: datetime):
    return filter_start_stop(cte.TABLE_NAME_CAREPLANS, start, stop)

def get_careplan_by_encounter_patient_ID(encounter_ID: str = None, patient_ID: str = None):
    return get_by_encounter_patient_ID(cte.TABLE_NAME_CAREPLANS, encounter_ID, patient_ID)


#Claims
def list_claims():
    return list_by_table_name(cte.TABLE_NAME_CLAIMS)

def get_claims_by_ID(id:str):
    return get_by_ID(cte.TABLE_NAME_CLAIMS, id)

def filter_claims_by_datetime(start: datetime, stop: datetime):
    query_filter = f'''SELECT * 
        FROM {cte.TABLE_NAME_CLAIMS}
        WHERE SERVICEDATE BETWEEN {start} AND {stop};
        '''
    findings = return_query(query_filter)
    return findings

def get_claims_by_patient_ID(patient_ID: str = None):
    return get_by_encounter_patient_ID(cte.TABLE_NAME_CLAIMS, None, patient_ID)


#Claims transactions
def list_claims_transactions():
    return list_by_table_name(cte.TABLE_NAME_CLAIMS_TRANSACTIONS)

def get_claims_transaction_by_ID(id:str):
    return get_by_ID(cte.TABLE_NAME_CLAIMS_TRANSACTIONS, id)

def filter_claims_transactions_by_datetime(start: datetime, stop: datetime):
    query_filter = f'''SELECT * 
        FROM {cte.TABLE_NAME_CLAIMS_TRANSACTIONS}
        WHERE FROMDATE < {start} AND TODATE > {stop};
        '''
    findings = return_query(query_filter)
    return findings

def get_claims_transactions_by_patient_ID(patient_ID: str = None):
    return get_by_encounter_patient_ID(cte.TABLE_NAME_CLAIMS_TRANSACTIONS, None, patient_ID)

#Conditions
def list_conditions():
    return list_by_table_name(cte.TABLE_NAME_CONDITIONS)

def filter_conditions_by_datetime(start: datetime, stop: datetime):
    return filter_start_stop(cte.TABLE_NAME_CONDITIONS, start, stop)

def get_conditions_by_encounter_patient_ID(encounter_ID: str = None, patient_ID: str = None):
    return get_by_encounter_patient_ID(cte.TABLE_NAME_CONDITIONS, encounter_ID, patient_ID)

#Encounters
def list_encounters():
    return list_by_table_name(cte.TABLE_NAME_ENCOUNTERS)

def get_encounter_by_ID(id:str):
    return get_by_ID(cte.TABLE_NAME_ENCOUNTERS, id)

def filter_encounters_by_datetime(start: datetime, stop: datetime):
    return filter_start_stop(cte.TABLE_NAME_ENCOUNTERS, start, stop)

def get_encounters_by_organization_ID(id: str):
    query_get_encounters = f'''SELECT ENCOUNTERCLASS, PATIENT, START, STOP, ORGANIZATION 
    FROM {cte.TABLE_NAME_ENCOUNTERS}
    WHERE ORGANIZATION = '{id}';
    '''
    encounters = return_query(query_get_encounters)
    return encounters

def get_encounter_by_patient_ID(patient_ID: str = None):
    return get_by_encounter_patient_ID(cte.TABLE_NAME_ENCOUNTERS, None, patient_ID)


#Imaging Studies
def list_imaging_studies():
    return list_by_table_name(cte.TABLE_NAME_IMAGING_STUDIES)

def get_imaging_study_by_ID(id:str):
    return get_by_ID(cte.TABLE_NAME_IMAGING_STUDIES, id)

def filter_imaging_studies_transactions_by_datetime(start: datetime, stop: datetime):
    query_filter = f'''SELECT * 
        FROM {cte.TABLE_NAME_IMAGING_STUDIES}
        WHERE DATE BETWEEN {start} AND {stop};
        '''
    findings = return_query(query_filter)
    return findings

def get_imaging_studies_by_encounter_patient_ID(encounter_ID: str = None, patient_ID: str = None):
    return get_by_encounter_patient_ID(cte.TABLE_NAME_IMAGING_STUDIES, encounter_ID, patient_ID)


#Immunizations
def list_immunizations():
    return list_by_table_name(cte.TABLE_NAME_IMMUNIZATIONS)

def filter_immunizations_by_datetime(start: datetime, stop: datetime):
    query_filter = f'''SELECT * 
        FROM {cte.TABLE_NAME_IMMUNIZATIONS}
        WHERE DATE BETWEEN {start} AND {stop};
        '''
    findings = return_query(query_filter)
    return findings

def get_immunizations_by_encounter_patient_ID(encounter_ID: str = None, patient_ID: str = None):
    return get_by_encounter_patient_ID(cte.TABLE_NAME_IMMUNIZATIONS, encounter_ID, patient_ID)


#Medications
def list_medications():
    return list_by_table_name(cte.TABLE_NAME_MEDICATIONS)

def filter_medications_by_datetime(start: datetime, stop: datetime):
    return filter_start_stop(cte.TABLE_NAME_MEDICATIONS, start, stop)

def get_medications_by_encounter_patient_ID(encounter_ID: str = None, patient_ID: str = None):
    return get_by_encounter_patient_ID(cte.TABLE_NAME_MEDICATIONS, encounter_ID, patient_ID)


#Observations
def list_observations():
    return list_by_table_name(cte.TABLE_NAME_OBSERVATIONS)

def get_observations_by_encounter_patient_ID(encounter_ID: str = None, patient_ID: str = None):
    return get_by_encounter_patient_ID(cte.TABLE_NAME_OBSERVATIONS, encounter_ID, patient_ID)


#Organizations
def list_organizations():
    return list_by_table_name(cte.TABLE_NAME_ORGANIZATIONS)

def get_organization_by_ID(id:str):
    return get_by_ID(cte.TABLE_NAME_ORGANIZATIONS, id)

#Patients
def list_patients():
    return list_by_table_name(cte.TABLE_NAME_PATIENTS)

def get_patient_by_ID(id:str):
    return get_by_ID(cte.TABLE_NAME_PATIENTS, id)

def filter_patients_by_datetime(start: datetime, stop: datetime):
    query_filter = f'''SELECT * 
        FROM {cte.TABLE_NAME_PATIENTS}
        WHERE BIRTHDATE > {start} AND DEATHDATE < {stop};
        '''
    findings = return_query(query_filter)
    return findings

#Payer transactions
def list_payer_transactions():
    return list_by_table_name(cte.TABLE_NAME_PAYER_TRANSITIONS)

def filter_payer_transactions_by_datetime(start: datetime, stop: datetime):
    query_filter = f'''SELECT * 
        FROM {cte.TABLE_NAME_PAYER_TRANSITIONS}
        WHERE START_DATE > {start} AND END_DATE < {stop};
        '''
    findings = return_query(query_filter)
    return findings

def get_payer_transaction_by_patient_ID(patient_ID: str = None):
    return get_by_encounter_patient_ID(cte.TABLE_NAME_PAYER_TRANSITIONS, None, patient_ID)


#Payers
def list_payers():
    return list_by_table_name(cte.TABLE_NAME_PAYERS)

def get_payer_by_ID(id:str):
    return get_by_ID(cte.TABLE_NAME_PAYERS, id)

#Procedures
def list_procedures():
    return list_by_table_name(cte.TABLE_NAME_PROCEDURES)

def filter_procedures_by_datetime(start: datetime, stop: datetime):
    return filter_start_stop(cte.TABLE_NAME_PROCEDURES, start, stop)

def get_procedures_by_encounter_patient_ID(encounter_ID: str = None, patient_ID: str = None):
    return get_by_encounter_patient_ID(cte.TABLE_NAME_PROCEDURES, encounter_ID, patient_ID)


#Providers
def list_providers():
    return list_by_table_name(cte.TABLE_NAME_PROVIDERS)

def get_provider_by_ID(id:str):
    return get_by_ID(cte.TABLE_NAME_PROVIDERS, id)

#Supplies
def list_supplies():
    return list_by_table_name(cte.TABLE_NAME_SUPPLIES)

def filter_supplies_by_datetime(start: datetime, stop: datetime):
    query_filter = f'''SELECT * 
        FROM {cte.TABLE_NAME_SUPPLIES}
        WHERE DATE BETWEEN {start} AND {stop};
        '''
    findings = return_query(query_filter)
    return findings

def get_supplies_by_encounter_patient_ID(encounter_ID: str = None, patient_ID: str = None):
    return get_by_encounter_patient_ID(cte.TABLE_NAME_SUPPLIES, encounter_ID, patient_ID)

