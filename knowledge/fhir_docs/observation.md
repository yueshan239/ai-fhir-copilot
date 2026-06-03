# FHIR Observation Resource

An Observation represents a measurement or simple assertion made about a patient, device, or other subject. It is the primary resource for clinical measurements including vital signs, lab results, and clinical findings.

## Key Fields

- `resourceType`: Always "Observation"
- `status`: registered | preliminary | final | amended | corrected | cancelled | entered-in-error | unknown
- `category`: Classification (vital-signs, laboratory, imaging, survey, etc.)
- `code`: What was observed (LOINC code preferred)
- `subject`: Reference to Patient, Group, Device, or Location
- `effective[x]: When the observation was made (effectiveDateTime, effectivePeriod)
- `value[x]: The result (valueQuantity, valueCodeableConcept, valueString, valueBoolean, valueRange, valueRatio)
- `dataAbsentReason`: Why no value
- `interpretation`: High, low, normal, abnormal
- `referenceRange`: Normal range for the result
- `component`: Sub-observations (e.g., systolic + diastolic blood pressure)

## Search Parameters

- `patient` / `subject`: Reference to patient
- `category`: Filter by category
- `code`: Filter by observation code
- `status`: Filter by status
- `date`: Filter by effective date
- `value-quantity`: Filter by numeric value

## Example (Vital Sign - Blood Pressure)

```json
{
  "resourceType": "Observation",
  "status": "final",
  "category": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/observation-category",
          "code": "vital-signs"
        }
      ]
    }
  ],
  "code": {
    "coding": [
      {
        "system": "http://loinc.org",
        "code": "85354-9",
        "display": "Blood pressure panel"
      }
    ]
  },
  "subject": {
    "reference": "Patient/123"
  },
  "effectiveDateTime": "2024-01-15T10:30:00Z",
  "component": [
    {
      "code": {
        "coding": [
          {
            "system": "http://loinc.org",
            "code": "8480-6",
            "display": "Systolic blood pressure"
          }
        ]
      },
      "valueQuantity": {
        "value": 120,
        "unit": "mmHg",
        "system": "http://unitsofmeasure.org",
        "code": "mm[Hg]"
      }
    },
    {
      "code": {
        "coding": [
          {
            "system": "http://loinc.org",
            "code": "8462-4",
            "display": "Diastolic blood pressure"
          }
        ]
      },
      "valueQuantity": {
        "value": 80,
        "unit": "mmHg",
        "system": "http://unitsofmeasure.org",
        "code": "mm[Hg]"
      }
    }
  ]
}
```
