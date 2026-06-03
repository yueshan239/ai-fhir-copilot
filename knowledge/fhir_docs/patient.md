# FHIR Patient Resource

The Patient resource represents demographic and other administrative information about an individual or animal receiving care or other health-related services.

## Key Fields

- `resourceType`: Always "Patient"
- `identifier`: An identifier for this patient
- `name`: A name associated with the patient
- `gender`: male | female | other | unknown
- `birthDate`: The date of birth (YYYY-MM-DD)
- `address`: An address for the individual
- `telecom`: A contact detail for the individual

## Example

```json
{
  "resourceType": "Patient",
  "identifier": [
    {
      "system": "http://hospital.example.com/patients",
      "value": "12345"
    }
  ],
  "name": [
    {
      "family": "Smith",
      "given": ["John"]
    }
  ],
  "gender": "male",
  "birthDate": "1990-01-15"
}
```
