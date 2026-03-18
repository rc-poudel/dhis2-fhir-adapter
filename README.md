# DHIS2 FHIR Adapter – Immunization Mapping

## Overview

This project maps FHIR **Immunization** resources (SNOMED-coded vaccines) into **DHIS2 Tracker** using FHIRPath expressions. It also explains how **Tracked Entity Instances (TEI)** are used to represent patients in DHIS2.

---

## FHIR Query Example

```http
GET Immunization?system=http://snomed.info/sct&code=390840006&display=Bacillus Calmette-Guérin vaccine
```

### Meaning

| Field   | Value                          |
| ------- | ------------------------------ |
| System  | SNOMED CT                      |
| Code    | 390840006                      |
| Vaccine | BCG (Bacillus Calmette-Guérin) |

---

## FHIR Resource Structure

```json
{
  "resourceType": "Immunization",
  "id": "immunization-bcg",
  "status": "completed",
  "vaccineCode": {
    "coding": [
      {
        "system": "http://snomed.info/sct",
        "code": "390840006",
        "display": "Bacillus Calmette-Guérin vaccine"
      }
    ]
  },
  "patient": {
    "reference": "Patient/123"
  },
  "occurrenceDateTime": "2025-03-12T00:00:00Z"
}
```

---

## FHIRPath Expressions

### Vaccine Code

```fhirpath
Immunization.vaccineCode.coding.where(system='http://snomed.info/sct').code
```

### Vaccine Display

```fhirpath
Immunization.vaccineCode.coding.where(system='http://snomed.info/sct').display
```

### Immunization Date

```fhirpath
Immunization.occurrenceDateTime
```

### Patient Reference

```fhirpath
Immunization.patient.reference
```

---

## DHIS2 Mapping Configuration

### Example: Data Element Mapping

```json
{
  "program": "IMMUNIZATION_PROGRAM",
  "programStage": "IMMUNIZATION_STAGE",
  "dataElements": [
    {
      "dataElement": "BCG_DOSE",
      "fhirPath": "Immunization.vaccineCode.coding.where(system='http://snomed.info/sct').code",
      "valueMappings": {
        "390840006": "BCG"
      }
    },
    {
      "dataElement": "IMMUNIZATION_DATE",
      "fhirPath": "Immunization.occurrenceDateTime"
    }
  ]
}
```

---

## TEI (Tracked Entity Instance) Mapping

### Purpose

TEI represents a **person/patient** in DHIS2.

### FHIR → TEI Mapping

| FHIR Field                  | DHIS2 Field                  | Description                           |
|------------------------------|------------------------------|---------------------------------------|
| Patient.id                   | trackedEntityInstance        | Unique identifier of the patient TEI  |
| Patient.name[0].given[0]     | Attribute (First Name)       | Patient’s first/given name            |
| Patient.name[0].family       | Attribute (Last Name)        | Patient’s family/last name            |
| Patient.gender               | Attribute (Gender)           | Patient gender (male/female/other)   |
| Patient.birthDate            | Attribute (DOB)              | Date of birth (YYYY-MM-DD)            |
| Patient.identifier[n].value  | Attribute (Identifier)       | Any additional identifiers            |

### Example TEI Payload

```json
{
  "trackedEntityType": "PERSON",
  "orgUnit": "ORG_UNIT_ID",
  "attributes": [
    {
      "attribute": "FIRST_NAME",
      "value": "Ram"
    },
    {
      "attribute": "GENDER",
      "value": "male"
    }
  ]
}
```

---

## Linking Immunization → TEI

### Step Flow

1. Extract patient reference:

```fhirpath
Immunization.patient.reference
```

2. Fetch patient resource from FHIR:

```http
GET /Patient/123
```

3. Map patient → TEI in DHIS2
4. Create an Event under the TEI

---

## Event Creation (DHIS2)

```json
{
  "trackedEntityInstance": "TEI_ID",
  "program": "IMMUNIZATION_PROGRAM",
  "programStage": "IMMUNIZATION_STAGE",
  "orgUnit": "ORG_UNIT_ID",
  "eventDate": "2025-03-12",
  "dataValues": [
    {
      "dataElement": "BCG_DOSE",
      "value": "BCG"
    }
  ]
}
```

---

## Value Mapping Strategy

DHIS2 does **not** understand SNOMED codes directly. Map codes manually:

| SNOMED Code | DHIS2 Value |
| ----------- | ----------- |
| 390840006   | BCG         |

---

## Optional: Filter Only BCG

```fhirpath
Immunization.vaccineCode.coding.where(
  system='http://snomed.info/sct' and code='390840006'
).exists()
```

---

## Adapter Flow (End-to-End)

1. Fetch Immunization from FHIR
2. Extract:

   * Vaccine code
   * Date
   * Patient reference
3. Fetch Patient from FHIR
4. Create/Match TEI
5. Create Event in DHIS2
6. Map values using lookup table

---

## Suggested Folder Structure

```
dhis2-fhir-adapter/
│
├── config/
│   ├── mapping.json
│   └── value_sets.json
│
├── services/
│   ├── fhir_client.py
│   ├── dhis2_client.py
│
├── transformers/
│   ├── immunization_mapper.py
│   └── patient_mapper.py
│
├── main.py
└── README.md
```

---

## Quick Start

```bash
# Install requirements
pip install -r requirements.txt

# Run adapter
python main.py
```

### Features

* FHIRPath-based mapping
* SNOMED → DHIS2 value mapping
* TEI creation from Patient
* Event creation from Immunization

---

## License

MIT License
