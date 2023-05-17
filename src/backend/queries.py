'''
    This module contains the available queries for the Firely server
'''

from datetime import datetime
import json
import os
from typing import Union
from dotenv import load_dotenv
import requests
import backend.utils
import pandas as pd

load_dotenv()

def build_query_with_filter(resource: str,
                            date_filter: bool,
                            date_from: Union[datetime, None],
                            date_to: Union[datetime, None],
                            filters: Union[dict, None]):
  '''Handles the query construction
  
  Args:
    resource: A string representing the name of the resource
    date_col: A boolean indicating if there is a filter by datetime
    date_from: An optional datetime representing the minimum date
    date_to: An optional datetime representing the maximum date
    filters: An optional dictionary representing the additional queries
  Returns:
    A string representing the request endpoint to call
  '''
  
  # Initialize query
  query = os.getenv("URL_SERVER")

  # Access resource
  query = query + resource

  #Construct additional queries
  if date_from and date_filter:
    query = query + '?date=ge'+date_from.strftime("%Y-%m-%d")
    if date_to and date_filter:
      query = query + '&date=le'+date_to.strftime("%Y-%m-%d")
  elif date_to and date_filter:
    query = query + '?date=le'+date_to.strftime("%Y-%m-%d")
  
  if filters:
    if not date_filter:
      query = query+'?'
    else:
      query = query+'&'
    for field, search_value in filters.items():
      query = query+field+'='+search_value+'&'
    query = query[:-1]  
  print(query)
  return query
     

def create_dataframe(dataframe: pd.DataFrame,
                     x_col: str,
                     y_col: Union[str,None],
                     list_fhir: list):
  '''Handles the data modeling
  Each resource data type is checked to access to the correct value
  A dataframe grows for each registry
    
    Args:
      dataframe: An empty dataframe
      x_col: A string representing the name of the first resource attribute
      y_col: An optional string representing the name of the second resource attribute
      list_fhir: A list of FHIR resources
    Returns:
      A dataframe containing the final values
  '''
  
  properties = list_fhir[0].elementProperties()

  x_data = [ (name, data_type, is_list) for name, name_json, data_type, is_list, of_many, not_optional in properties if name == x_col]
  x_access = "['"+x_col+"']"
  
  with open('static/dicts/resource_variables.json') as fp:
    keys_FHIR = json.load(fp)

  if x_data[0][1] != str and x_data[0][1] != int and x_data[0][1].resource_type in keys_FHIR['DATA_TYPE'].keys():
    if x_data[0][2]:
      x_access = x_access+"[0]"
    x_access = x_access+keys_FHIR['DATA_TYPE'][x_data[0][1].resource_type]

  if y_col:
    y_data = [ (name, data_type, is_list) for name, name_json, data_type, is_list, of_many, not_optional in properties if name == y_col]
    y_access = "['"+y_col+"']"
    if y_data[0][1] != str and y_data[0][1] != int and y_data[0][1].resource_type in keys_FHIR['DATA_TYPE'].keys():
          if y_data[0][2]:
              y_access = y_access+"[0]"
          y_access = y_access+keys_FHIR['DATA_TYPE'][y_data[0][1].resource_type]
  
  for registry in list_fhir:
      registry_as_json = registry.as_json()
      x_value = eval("registry_as_json"+x_access) if registry_as_json.get(x_col) else None
      y_value = eval("registry_as_json"+y_access) if y_col and registry_as_json.get(y_col) else None
      dataframe.loc[len(dataframe)] = [str(x_value), y_value]

  return dataframe


def query_firely_server(resource: str,
                        x: str,
                        date_filter: bool,
                        date_from: Union[datetime, None],
                        date_to: Union[datetime, None],
                        y: Union[str,None] = None,
                        filters: dict = None):
    '''Handles the query of a given resource to Firely server
    and the retrieval of the response in an interpretable form
    Calls the function responsible of building the endpoint
    Calls the function responsible of modelling the request response
    
    Args:
      resource: A string representing the name of the resource
      x: A string representing the name of the first resource attribute
      date_col: A boolean indicating if there is a filter by datetime
      date_from: An optional datetime representing the minimum date
      date_to: An optional datetime representing the maximum date
      y: An optional string representing the name of the second resource attribute
      filters: An optional dictionary representing the additional queries
    
    Raises:
      TypeError if the request is not successful
    Returns:
      A dataframe with the resource information filtered
    '''

    query = build_query_with_filter(resource=resource, date_filter=date_filter, date_from=date_from, date_to=date_to, filters=filters)
    
    result = requests.get(query)
    
    if result.status_code and result.status_code==200:
        list_registries = []
        dataframe = pd.DataFrame(columns = [x, y])
        bundle = result.json()
        if bundle['total']:
            for entry in list(bundle['entry']):
                if entry['resource']['resourceType']=='OperationOutcome':
                  print('This resource does not support this filter!')
                else:
                  registry = eval("backend.utils."+resource.lower()+"."+resource+"(entry['resource'])")
                  list_registries.append(registry)
            dataframe = create_dataframe(dataframe,x,y,list_registries)
        return dataframe

    result.raise_for_status()



# Define the input parameters from frontend/ploty

# with open('src/backend/FHIR_dict.json') as fp:
#   keys_FHIR = json.load(fp)
# keys_FHIR.pop('DATA_TYPE')
# filter_FHIR = keys_FHIR.get("FILTER_PARAMS")
# keys_FHIR.pop("FILTER_PARAMS")
# list_resources = keys_FHIR.keys()
# b = None
# date_attribute = True
# date_from=datetime(2022,5,23,0,0,0)
# date_to=datetime(2023,5,10,0,0,0)
# for resource in list_resources:
#   a = keys_FHIR.get(resource)[0].keys()
#   dict_filter = {}
#   list_filters = filter_FHIR.get(resource)
#   for f in list_filters:
#      dict_filter[f] = 'test'
#   [print(query_firely_server(resource, x, date_attribute, date_from, date_to, b, dict_filter)) for x in a] 
