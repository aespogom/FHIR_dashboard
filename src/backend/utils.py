from fhirclient import client

# Create an instance of the FHIR client
settings = {
    'api_base': 'firelyasserver.azurewebsites.net'
}
smart = client.FHIRClient(settings=settings)

