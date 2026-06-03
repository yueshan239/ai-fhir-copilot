# FHIR Encounter Resource

An Encounter represents an interaction between a patient and healthcare provider(s) for the purpose of providing healthcare services or assessing the health status of a patient.

## Key Fields

- `resourceType`: Always "Encounter"
- `status`: planned | arrived | triaged | in-progress | onleave | finished | cancelled | entered-in-error | unknown
- `class`: Classification (AMB - ambulatory, EMER - emergency, IMP - inpatient, etc.)
- `type`: Specific type of encounter
- `subject`: Reference to Patient
- `participant`: List of participants (practitioner, etc.)
- `period`: Start and end time
- `reasonCode`: Why the encounter takes place
- `diagnosis`: The list of diagnosis relevant to this encounter
- `hospitalization`: Details about admission

## Search Parameters

- `patient` / `subject`: Reference to patient
- `status`: Filter by status
- `class`: Filter by encounter class
- `date`: Filter by period
- `type`: Filter by encounter type
- `reason-code`: Filter by reason

## Example

```json
{
  "resourceType": "Encounter",
  "status": "finished",
  "class": {
    "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
    "code": "IMP",
    "display": "inpatient encounter"
  },
  "type": [
    {
      "coding": [
        {
          "system": "http://snomed.info/sct",
          "code": "183807002",
          "display": "Inpatient stay"
        }
      ]
    }
  ],
  "subject": {
    "reference": "Patient/123"
  },
  "participant": [
    {
      "individual": {
        "reference": "Practitioner/456"
      }
    }
  ],
  "period": {
    "start": "2024-01-15T08:00:00Z",
    "end": "2024-01-20T10:00:00Z"
  },
  "reasonCode": [
    {
      "coding": [
        {
          "system": "http://snomed.info/sct",
          "code": "44054006",
          "display": "Type 2 diabetes mellitus"
        }
      ]
    }
  ]
}
```
