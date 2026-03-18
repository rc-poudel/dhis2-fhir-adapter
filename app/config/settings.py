import os
from dotenv import load_dotenv

load_dotenv()

DHIS2_API_URL = os.getenv("DHIS2_API_URL")
DHIS2_USERNAME = os.getenv("DHIS2_USERNAME")
DHIS2_PASSWORD = os.getenv("DHIS2_PASSWORD")
DHIS2_PROGRAM = os.getenv("DHIS2_PROGRAM")
DHIS2_ORG_UNIT = os.getenv("DHIS2_ORG_UNIT")
TRACKED_ENTITY_TYPE = os.getenv("TRACKED_ENTITY_TYPE")
FHIR_ATTRIBUTE_ID = os.getenv("FHIR_ATTRIBUTE_ID")