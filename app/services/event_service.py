from app.clients.dhis2_client import get_events
from app.mappings.data_element import get_fhir_data_elements
from app.transformers.resource_transformer import transform_to_resource
import json

def get_all_fhir_events():
    events = get_events()
    fhir_data_element = get_fhir_data_elements()
    resources = []
    for event in events:
        resource = transform_to_resource(event, fhir_data_element)
        if resource:
            resources.append(resource)
    return resources