# FHIR Condition Resource

A Condition represents a clinical condition, problem, diagnosis, or other event, situation, issue, or clinical concept that has risen to a level of concern.

## Key Fields

- `resourceType`: Always "Condition"
- `clinicalStatus`: active | recurrence | relapse | inactive | remission | resolved | entered-in-error | unknown
- `verificationStatus`: confirmed | provisional | differential | refuted | entered-in-error | unknown
- `category`: problem-list-item | encounter-diagnosis | health-concern
- `severity`: Severity code (mild, moderate, severe)
- `code`: Identification of the condition (SNOMED CT, ICD-10)
- `bodySite`: Anatomical location
- `subject`: Reference to Patient or Group
- `encounter`: Reference to Encounter when recorded
- `onsetDateTime`: When condition first occurred
- `abatementDateTime`: When condition resolved

## Search Parameters

- `patient` / `subject`: Reference to patient
- `clinical-status`: Filter by clinical status
- `verification-status`: Filter by verification status
- `category`: Filter by category
- `code`: Filter by condition code
- `severity`: Filter by severity
- `onset-date`: Filter by onset date

## Example

```json
{
  "resourceType": "Condition",
  "clinicalStatus": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
        "code": "active"
      }
    ]
  },
  "verificationStatus": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
        "code": "confirmed"
      }
    ]
  },
  "category": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/condition-category",
          "code": "encounter-diagnosis"
        }
      ]
    }
  ],
  "code": {
    "coding": [
      {
        "system": "http://snomed.info/sct",
        "code": "44054006",
        "display": "Type 2 diabetes mellitus"
      }
    ]
  },
  "subject": {
    "reference": "Patient/123"
  },
  "encounter": {
    "reference": "Encounter/789"
  },
  "onsetDateTime": "2020-03-15"
}
```
