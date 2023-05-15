'''
    This module contains the logic to preload the server with FHIR resources
    located at src/database/data/synthea_output/fhir.
    
    ATTENTION! First, update USER_PATH with your local path.
    ATTENTION! Second, in src/database/data/synthea_output/zip folder.
        They will be deleted after the execution.
    For more information, https://docs.fire.ly/projects/Firely-Server/en/latest/maintenance/preload.html
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

isExist = os.path.exists(mypath+"/resources")
if not isExist:
    os.makedirs(mypath+"/resources")

onlyfiles = [f for f in listdir(mypath+"/zip") if isfile(join(mypath+"/zip", f))]  
for file_name in onlyfiles:
    # Opening JSON file
    f = open(mypath+'/zip/'+file_name)
    
    # returns JSON object as a dictionary
    try:
        data = json.load(f)
        
        # Iterating through the json list
        for resource in data['entry']:
            with open(mypath+'/resources/'+file_name.replace('.json','')+resource['request']['url']+'.json', 'w') as fp:
                json.dump(resource['resource'], fp, ensure_ascii=False)
        
                # Closing file
                fp.close()
        f.close()
    except:
        print('error in '+ file_name)
shutil.rmtree(mypath+"/zip")
print('--------------FINISHED---------------')
