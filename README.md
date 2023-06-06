# MedDash App

![Logo](https://github.com/aespogom/FHIR_dashboard/blob/dev/src/static/img/Med2.png.png)


MedDash project is designed to allow hospitals to easily monitor data from any resource in a single location. It uses the Fast Healthcare Interoperability Resources (FHIR) standard to transfer patient data from a Firely server hosted in Azure Web App Services. For the web-based dashboard interface, it is built in Flask framework along with the Plotly library.

The dashboard can be easily customized to meet the needs of different hospital departments, with options to select which data resources to display, how the data is displayed, filter by any attribute or resource, and other features.

One of the key advantages of this project is its generalizability. With the use of FHIR, the dashboard can easily connect to various electronic health record (EHR) systems and other healthcare data sources. This means that hospitals and healthcare organizations of all sizes and specialties can use the dashboard to monitor and manage their data, regardless of their existing infrastructure. The only requirement is FHIR protocol.

The dashboard can be configured to display graphs that highlight trends, patterns, and insights that may be difficult to discern from raw data alone. This enables healthcare providers to quickly identify potential issues, such as spikes in patient activity or concerning changes in vital signs, and take action as needed.

Additionally, ChatGPT API is integrated in the application. A user can use the prompt to automatically display the desired graph. Thanks to the standarization in FHIR, it is easy to extract from a simple prompt which resource, atttributes and filters the user is inserting.


![Architecture](https://github.com/aespogom/FHIR_dashboard/blob/dev/Architecture.png)

## Getting started
1. Clone the repository 
2. Navigate to the project `/src/`
3. Create a virtual environment
4. Install the required dependencies
5. Ask for the .env file to the team
6. Run the project

## Dependencies
Before running the application, you will need to have the following installed:

- Python 3.9
- Pip 23.0

Then, run the following command in your terminal:
```
pip install -r requirements.txt
```


## Running the Application
To run the application, navigate to the project directory (within `/src/`) in your terminal and run the following command:

```
python -m flask run --debug 
```

This will start the Flask development server and the application will be available at http://localhost:5000.


## For Developers
### Backend advance search examples
The following list is a set of examples that the frontend can include in
the call query_firely_server from src/backend/queries.py

0. No query:

    query_firely_server(resource, x, date_filter, y):
        
        - resource (string): 'AdverseEvent'
        - x (string): 'actuality'
        - date_filter (bool): False
        - y (string, optional): 'code'
    
    resulting endpoint: [URL_SERVER]/AdverseEvent

1. Simple query by datetime:
    
    query_firely_server(resource, x, date_filter, date_from, date_to, y, dict_filter):
        
        - resource (string): 'AdverseEvent'
        - x (string): 'actuality'
        - date_filter (bool): True
        - date_from (datetime, optional): datetime(2022, 5, 1, 0, 0)
        - date_to (datetime, optional): datetime(2022, 5, 23, 0, 0)
        - y (string, optional): None
    
    resulting endpoint: `[URL_SERVER]`/AdverseEvent?date=ge2022-05-01&date=le2023-05-23

2. Advance query by datetime + relate to other resource:
    
    query_firely_server(resource, x, date_filter, date_from, date_to, y, dict_filter):
        
        - resource (string): 'AdverseEvent'
        - x (string): 'actuality'
        - date_filter (bool): True
        - date_from (datetime, optional): datetime(2022, 5, 1, 0, 0)
        - date_to (datetime, optional): datetime(2022, 5, 23, 0, 0)
        - y (string, optional): None
        - dict_filter (dict, optional): {
            'actuality': 'test', 
            'category': 'test', 
            'code': 'test', 
            'patient': {
                'gender': 'other',
                'family': 'Donald'
            },
            'Observation': {
                'code': 'ABC-DEF'
            }
        }

    resulting endpoint: `[URL_SERVER]`/AdverseEvent?date=ge2022-05-1&date=le2023-05-23&actuality=test&category=test&code=test&patient.gender=other&patient.family=Donald&patient._has:Observation:patient:code=ABC-DEF


### Contributing
If you'd like to contribute to this project, please fork the repository and submit a pull request.
1. Fork the Project
2. Create your Feature Branch (git checkout -b feature/AmazingFeature)
3. Commit your Changes (git commit -m 'Add some AmazingFeature')
4. Push to the Branch (git push origin feature/AmazingFeature)
5. Open a Pull Request
