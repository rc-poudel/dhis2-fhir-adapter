from fhir.resources.immunization import Immunization
from urllib.parse import urlparse, parse_qs

def transform_to_resource(data_item, mappings):

    sample_path = mappings[0].get("fhirPath", "")
    
    if sample_path.startswith("Immunization"):
        return transform_event_to_immunization(data_item, mappings)
    
    return None

def transform_event_to_immunization(event, fhir_des):

    data_values = event.get("dataValues", [])
    if not data_values:
      return None

    vaccine_code_data = None

    for de_mapping in fhir_des:
        dv = next((d for d in data_values if d["dataElement"] == de_mapping["id"]), None)
        
        if dv and dv.get("value"):
            path = de_mapping["fhirPath"]
            
            if "Immunization?" in path:
                params = parse_qs(path.split("?")[-1])
                vaccine_code_data = {
                    "coding": [{
                        "system": params.get('system', [None])[0],
                        "code": params.get('code', [None])[0],
                        "display": params.get('display', [None])[0]
                    }]
                }
                break 

    if not vaccine_code_data:
        # print(f"Skipping event {event.get('event')}: No matching vaccineCode mapping found.")
        return None
    # print(event)
    imm = Immunization(
        id=event.get("event"),
        status="completed",
        vaccineCode=vaccine_code_data,
        patient={"reference": f"Patient/{event.get('trackedEntityInstance')}"},
        occurrenceDateTime=event.get("occurredAt") + "Z"
    )
    
    return imm