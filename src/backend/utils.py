from fhirclient import client

# Create an instance of the FHIR client
settings = {
    'api_base': 'firelyasserver.azurewebsites.net',
    'app_id': 'app'
}
smart = client.FHIRClient(settings=settings)

