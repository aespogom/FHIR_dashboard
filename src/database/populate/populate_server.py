'''
    This module contains the logic to populate the server with FHIR resources
    located at src/database/data/synthea_output/fhir.
    
    ATTENTION! First, update USER_PATH with your local path.
    ATTENTION! Second, unzip src/database/data/synthea_output/fhir.zip
        in src/database/data/synthea_output/zip folder.
        They will be deleted after the execution.
'''

import json
from os import listdir
import os
from os.path import isfile, join
import shutil
import requests
from dotenv import load_dotenv

load_dotenv()

USER_PATH = 'C:/Users/anaes/FHIR_dashboard/'

mypath = USER_PATH+'src/database/data/synthea_output'
url_server = os.getenv("URL_SERVER")
headers = {
  'Content-Type': 'application/json',
  'Cookie': 'ARRAffinity=92ca53ad8db4fbb93d4d3b7d8ab54dcf8ffecb2d731f25b0e91ad575d7534c3f; ARRAffinitySameSite=92ca53ad8db4fbb93d4d3b7d8ab54dcf8ffecb2d731f25b0e91ad575d7534c3f'
} 

isExist = os.path.exists(mypath+"/zip")
if not isExist:
    os.makedirs(mypath+"/zip")

onlyfiles = [f for f in listdir(mypath+"/zip") if isfile(join(mypath+"/zip", f))]  
for file_name in onlyfiles:
    # Opening JSON file
    f = open(mypath+'/zip/'+file_name)
    
    # returns JSON object as a dictionary
    data = json.load(f)
    
    # Iterating through the json list
    for resource in data['entry']:
        url = url_server + resource['request']['url'] +'/'+ resource['resource']['id']
        # url = "URL_SERVER/ResourceName/id"
        payload = json.dumps(resource['resource'])

        response = requests.request("PUT", url, headers=headers, data=payload)
        if not response.status_code or (response.status_code != 201 and response.status_code != 200):
            print('FAILED '+url)
        # else:
        #     print('OK '+resource['request']['url'] +'/'+ resource['resource']['id'])
    
    # Closing file
    f.close()
shutil.rmtree(mypath+"/zip")
print('--------------FINISHED---------------')
