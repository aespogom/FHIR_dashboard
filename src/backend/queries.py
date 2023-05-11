'''
    This module contains all the available queries for the Firely server
'''

from datetime import datetime
import os
from typing import Union
from dotenv import load_dotenv
import requests
import utils

load_dotenv()

def query_firely_server(resource: str,
                        x: str,
                        y: str,
                        date_col: Union[str, None],
                        date_from: Union[datetime, None],
                        date_to: Union[datetime, None]):
    # Initialize query
    query = os.getenv("URL_SERVER")

    # Access resource
    resource = resource.lower().capitalize()
    query = query + resource

    # Construct the datetime query
    if date_from and date_col:
        query = query + '?'+date_col+'=$gte='+date_from.strftime("%Y-%m-%d")
    if date_to and date_col:
        query = query + '?'+date_col+'=$lte='+date_to.strftime("%Y-%m-%d")

    # Perform the search
    result = requests.get(query)

    #TODO model
    if result.status_code and result.status_code==200:
        list_registries = []
        bundle = result.json()
        # Skip last element which is always the OperationOutcome
        for entry in list(bundle['entry'])[:-1]:
            registry = eval("utils."+resource.lower()+"."+resource+"(entry['resource'])")
            list_registries.append(registry)
    
        return list_registries

    return result

# # Define the input parameters from frontend/ploty
# resource = 'Observation'
# x = 'category'
# y = 'valueQuantity'
# date_attribute = 'effectiveDateTime'
# date_from=datetime(2023,5,1,0,0,0)
# date_to=datetime(2023,5,10,0,0,0)
# r = query_firely_server(resource, x, y, date_attribute, date_from, date_to)
# print(r)




