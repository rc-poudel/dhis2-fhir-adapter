import os
import requests

from app.config.settings import (
    DHIS2_API_URL,
    DHIS2_USERNAME,
    DHIS2_PASSWORD,
    DHIS2_PROGRAM,
    DHIS2_ORG_UNIT,
    TRACKED_ENTITY_TYPE,
    FHIR_ATTRIBUTE_ID
)

def get_fhir_data_elements():
    url = f"{DHIS2_API_URL}/api/dataElements"
    params = {
        "paging": "false",
        "fields": "id,name,valueType,attributeValues[attribute,value]"
    }

    response = requests.get(url, auth=(DHIS2_USERNAME, DHIS2_PASSWORD), params=params)

    fhir_elements = []

    if response.status_code == 200:
        elements = response.json().get("dataElements", [])
        for elem in elements:
            for av in elem.get("attributeValues", []):
                if av.get("attribute", {}).get("id") == FHIR_ATTRIBUTE_ID:
                    fhir_elements.append({
                        "id": elem["id"],
                        "name": elem["name"],
                        "valueType": elem["valueType"],
                        "fhirPath": av.get("value")
                    })
    else:
        print("Error fetching DEs:", response.text)

    return fhir_elements