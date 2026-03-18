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

def get_fhir_attributes():
    url = f"{DHIS2_API_URL}/api/trackedEntityAttributes"
    params = {
        "paging": "false",
        "fields": "id,name,valueType,attributeValues[attribute,value]"
    }

    response = requests.get(url, auth=(DHIS2_USERNAME, DHIS2_PASSWORD), params=params)

    fhir_attributes = []

    if response.status_code == 200:
        attributes = response.json().get("trackedEntityAttributes", [])
        for attr in attributes:
            for av in attr.get("attributeValues", []):
                if av.get("attribute", {}).get("id") == FHIR_ATTRIBUTE_ID:
                    fhir_attributes.append({
                        "id": attr["id"],
                        "name": attr["name"],
                        "valueType": attr["valueType"],
                        "fhirPath": av.get("value")
                    })
    else:
        print("Error fetching TEAs:", response.text)

    return fhir_attributes