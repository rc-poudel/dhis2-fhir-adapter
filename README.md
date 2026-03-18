# DHIS2 to FHIR Adapter (Python)

A Python-based middleware service that extracts data from DHIS2 and converts it into FHIR resources for interoperability with modern health systems.

This project enables integration between **DHIS2** and **FHIR-based systems**, allowing DHIS2 tracker data (Tracked Entities, Events, and Data Elements) to be transformed into FHIR resources such as Patient, Encounter, Observation, and QuestionnaireResponse.

---

## Overview

This project is a Python-based integration service that retrieves data from DHIS2 Tracker API and transforms it into FHIR-compliant resources (Patient, Immunization, Observation).
It enables interoperability between DHIS2 and FHIR-based systems.

**Workflow**
DHIS2 API → Python Adapter → Data Mapping → FHIR Server


---

## Features

- Fetch tracker events from DHIS2
- Transform DHIS2 data into FHIR resources
- Send resources to a FHIR server
- Configurable mapping layer
- Lightweight Python implementation
- Ready for integration with health data platforms

---

## Technologies Used

- Python 3.9+
- requests
- fhir.resources
- FastAPI (optional)

---

## Project Structure
project/
│
├── app/
│   ├── config/
│   │   └── settings.py
│   ├── services/
│   │   └── dhis2_service.py
│   ├── transformers/
│   │   └── fhir_mapper.py
│   ├── clients/
│   │   └── dhis2_client.py
│
├── main.py
├── requirements.txt
└── README.md

---

## Installation

Clone the repository

```bash
git clone <repo-url>
cd project

python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```
### Install dependencies

pip install -r requirements.txt