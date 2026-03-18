from app.clients.dhis2_client import get_tei
from app.mappings.tracked_entity import get_fhir_attributes
from app.transformers.patient_transformer import transform_tei_to_patient
import json

def get_all_fhir_patients():
    teis = get_tei()
    fhir_teas = get_fhir_attributes()

    patients = []
    for tei in teis:
        patient = transform_tei_to_patient(tei, fhir_teas)
        patients.append(patient)

    return patients