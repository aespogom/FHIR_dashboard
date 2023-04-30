'''
    This module contains shared logic for queries
'''
from datetime import datetime
from database.populate.database_connection import return_query

def list_by_table_name(table_name: str):
    '''Hadles the listing of the complete table information
    from a table name
    Args:
        table_name: A string representing given table
    Returns:
        A list of all the findings from the given table
    '''
    query_list = f'''SELECT *
    FROM {table_name}
    '''
    findings = return_query(query_list)
    return findings

def get_by_ID(table_name: str, id: str):
    '''Hadles the retrieval of the finding
    from a given table name and an ID
    Args:
        table_name: A string representing given table
        id: A string representign the ID to be matched
    Returns:
        A list of all the findings from the given table
    '''
    query_get = f'''SELECT * 
    FROM {table_name}
    WHERE ID = '{id}';
    '''
    findings = return_query(query_get)
    return findings

def get_by_encounter_patient_ID(table_name: str, encounter_ID: str = None, patient_ID: str = None):
    '''Hadles the retrieval of the finding
    from a given table name and an encounter and/or patient ID
    Args:
        table_name: A string representing given table
        encounter_id: A string representing the encounter ID to be matched
        patient_id: A string representing the patient ID to be matched
    Returns:
        A list of all the findings from the given table matching the ID(s)
    '''
    if encounter_ID and patient_ID:
        query_get = f'''SELECT * 
        FROM {table_name}
        WHERE ENCOUNTER = '{encounter_ID}' AND PATIENT = '{patient_ID}';
        '''
    elif encounter_ID and not patient_ID:
        query_get = f'''SELECT * 
        FROM {table_name}
        WHERE ENCOUNTER = '{encounter_ID}';
        '''
    elif not encounter_ID and patient_ID:
        query_get = f'''SELECT * 
        FROM {table_name}
        WHERE PATIENT = '{patient_ID}';
        '''
    findings = return_query(query_get)
    return findings

def filter_start_stop(table_name: str, start: datetime, stop: datetime):
    '''Hadles the filtering of findings from a given datetime
    to a given datetime from a given table name
    Args:
        table_name: A string representing given table
        start: A datetime representing the 'from' date
        stop: A datetime representing the 'to' date
    Returns:
        A list of all the findings from the given table that matches
        the from and to dates
    '''
    check_start = f'''SELECT * FROM sys.columns 
        WHERE [name] = 'START' AND [object_id] = OBJECT_ID('{table_name}');'''
    
    check_stop = f'''SELECT * FROM sys.columns 
        WHERE [name] = 'STOP' AND [object_id] = OBJECT_ID('{table_name}');'''
    
    if len(check_start) and len(check_stop):
        query_filter = f'''SELECT * 
        FROM {table_name}
        WHERE START > {start} AND STOP < {stop};
        '''
    elif len(check_start):
        query_filter = f'''SELECT * 
        FROM {table_name}
        WHERE START > {start};
        '''
    elif len(check_stop):
        query_filter = f'''SELECT * 
        FROM {table_name}
        WHERE STOP < {stop};
        '''
    findings = return_query(query_filter)
    return findings
