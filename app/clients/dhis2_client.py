import requests
import base64
from app.config.settings import (
    DHIS2_API_URL,
    DHIS2_USERNAME,
    DHIS2_PASSWORD,
    DHIS2_PROGRAM,
    DHIS2_ORG_UNIT,
    TRACKED_ENTITY_TYPE
)

def get_headers():
    auth_str = f"{DHIS2_USERNAME}:{DHIS2_PASSWORD}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    return {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/json"
    }

def get_tei():
    
    url = f"{DHIS2_API_URL}/api/tracker/trackedEntities"

    params = {
        "trackedEntityType" : {TRACKED_ENTITY_TYPE},
        "ouMode" : "ALL",
        "fields": "trackedEntity,attributes[attribute,value]",
        "pageSize": 2,
        "order": "createdAt:desc"

        # "trackedEntityType" : "CWkDesHkKCs",
        # "ouMode" : "ALL",
        # "fields": "trackedEntity,attributes[attribute,value]",
        # "paging": 'false',
        # "createdWithin" : '1d'
    }

    response = requests.get(url, headers=get_headers(), params=params)

    response.raise_for_status()

    tei = response.json().get("trackedEntities", [])

    return tei


def get_events():
    url = f"{DHIS2_API_URL}/api/tracker/events"

    params = {
        "ouMode": "ACCESSIBLE", 
        # "paging": "false",
        "pageSize": 2,
        "order": "occurredAt:desc",
        "fields": "event,trackedEntityInstance,program,occurredAt,dataValues[dataElement,value]"
    }

    response = requests.get(url, headers=get_headers(), params=params)
    response.raise_for_status()

    events = response.json().get("events", [])
    return events