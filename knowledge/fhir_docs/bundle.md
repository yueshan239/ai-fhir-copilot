# FHIR Bundle Resource

A Bundle is a container for a collection of resources. It is used to group related resources together for transmission, persistence, or transaction processing.

## Key Fields

- `resourceType`: Always "Bundle"
- `type`: document | message | transaction | transaction-response | batch | batch-response | history | searchset | collection
- `total`: Total number of matches (for searchset)
- `entry`: Array of entries, each containing:
  - `fullUrl`: The full URL of the resource
  - `resource`: The actual FHIR resource
  - `request`: For transaction/batch - the HTTP method and URL
  - `response`: For transaction-response - the server response

## Bundle Types

- **document**: A set of resources composed into a single clinical document
- **message**: A communication between systems
- **transaction**: A set of actions to be performed as a single atomic operation
- **batch**: A set of independent actions to be performed
- **searchset**: Results of a search operation
- **collection**: A curated collection of resources

## Transaction Example

```json
{
  "resourceType": "Bundle",
  "type": "transaction",
  "entry": [
    {
      "fullUrl": "urn:uuid:patient-1",
      "resource": {
        "resourceType": "Patient",
        "name": [{"family": "Smith", "given": ["John"]}],
        "gender": "male",
        "birthDate": "1990-01-15"
      },
      "request": {
        "method": "POST",
        "url": "Patient"
      }
    },
    {
      "fullUrl": "urn:uuid:encounter-1",
      "resource": {
        "resourceType": "Encounter",
        "status": "finished",
        "class": {
          "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
          "code": "AMB"
        },
        "subject": {
          "reference": "urn:uuid:patient-1"
        }
      },
      "request": {
        "method": "POST",
        "url": "Encounter"
      }
    },
    {
      "fullUrl": "urn:uuid:condition-1",
      "resource": {
        "resourceType": "Condition",
        "clinicalStatus": {
          "coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active"}]
        },
        "code": {
          "coding": [{"system": "http://snomed.info/sct", "code": "44054006", "display": "Type 2 diabetes mellitus"}]
        },
        "subject": {
          "reference": "urn:uuid:patient-1"
        }
      },
      "request": {
        "method": "POST",
        "url": "Condition"
      }
    }
  ]
}
```

## Search Result Bundle Example

```json
{
  "resourceType": "Bundle",
  "type": "searchset",
  "total": 2,
  "entry": [
    {
      "fullUrl": "https://example.com/fhir/Patient/123",
      "resource": {
        "resourceType": "Patient",
        "id": "123",
        "name": [{"family": "Smith", "given": ["John"]}]
      },
      "search": {"mode": "match"}
    }
  ]
}
```
