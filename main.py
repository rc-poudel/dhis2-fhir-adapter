import json
from fhir.resources.bundle import Bundle, BundleEntry
from app.services.tei_service import get_all_fhir_patients
from app.services.event_service import get_all_fhir_events

if __name__ == "__main__":

    patients = get_all_fhir_patients()
    clinical_data = get_all_fhir_events()

    all_resources = patients + clinical_data

    if not all_resources:
        print("No resources found with FHIR mappings.")
    else:
        entries = []
        for p in all_resources:
            entries.append(BundleEntry(resource=p))

        fhir_bundle = Bundle(type="collection", entry=entries)

        print(fhir_bundle.model_dump_json(indent=2))