import re
from fhir.resources.patient import Patient
from fhir.resources.humanname import HumanName
from fhir.resources.identifier import Identifier
from datetime import datetime

def apply_fhir_path(patient: Patient, path: str, value: str):

    if not value:
        return

    if path == "Patient.birthDate":
        try:
            patient.birthDate = value if datetime.strptime(value, '%Y-%m-%d').date() <= datetime.now().date() else None
        except (ValueError, TypeError):
            patient.birthDate = None

    elif path == "Patient.gender":
        patient.gender = value.lower()

    elif path == "Patient.name[0].given[0]":
        if not patient.name:
            patient.name = [HumanName()]
        patient.name[0].given = [value]

    elif path == "Patient.name[0].family":
        if not patient.name:
            patient.name = [HumanName()]
        patient.name[0].family = value

    match = re.match(r"Patient\.identifier\[\d+\]\.value", path)
    if match:
        if patient.identifier is None:
            patient.identifier = []

        new_identifier = Identifier(value=value)

        if "system=" in path:
            new_identifier.system = path.split("system=")[-1]

        patient.identifier.append(new_identifier)
        return

def transform_tei_to_patient(tei, fhir_teas):
    patient = Patient(
        id=tei.get("trackedEntityInstance"),
        active=True
    )

    tei_attributes = tei.get("attributes", [])

    for tea in fhir_teas:
        attr_data = next(
            (a for a in tei_attributes if a["attribute"] == tea["id"]),
            None
        )
        
        if attr_data and attr_data.get("value"):
            apply_fhir_path(patient, tea["fhirPath"], attr_data["value"])
    return patient