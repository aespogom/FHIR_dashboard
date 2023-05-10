'''
    This module contains all the available queries for the Firely server
'''

from utils import smart
from fhirclient.models import *


# Define the input parameters from frontend/ploty
resource = 'Observation'
x = 'category'
y = 'valueQuantity'
date_attribute = 'effectiveDateTime'
date_from='2023-05-01T00:00:00Z'
date_to='2023-05-10T00:00:00Z'

def query_firely_server(resource, x, y, date_col, date_from, date_to):
    # Construct the datetime query
    search_params = {
        date_attribute: {"$gte": date_from},
        date_attribute: {"$lte": date_to}
    }

    # Create a search query for the specified resource type
    query = getattr(smart, resource).where(params=search_params)

    # Perform the search
    result = query.perform_resources()

    #TODO model
    return result

query_firely_server(resource, x, y, date_attribute, date_from, date_to)




