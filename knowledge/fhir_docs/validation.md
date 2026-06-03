# FHIR Resource Validation

FHIR resources must conform to the specification for structure, cardinality, data types, and terminology bindings.

## Validation Levels

### Structural Validation
- Valid JSON or XML format
- Correct resourceType
- Required elements present
- Correct data types for each element

### Content Validation
- Coded values from required/expected value sets
- References point to valid resources
- Invariants (conditions across elements) are satisfied

### Profile Validation
- Conforms to StructureDefinition profiles
- Meets slicing requirements
- Satisfies profile-specific constraints

## Common Validation Rules

### Required Elements
- `Patient`: resourceType, name (at least one)
- `Encounter`: resourceType, status, class, subject
- `Condition`: resourceType, subject (clinicalStatus or verificationStatus recommended)
- `Observation`: resourceType, status, code, subject

### Data Type Rules
- `dateTime`: ISO 8601 format (YYYY-MM-DDThh:mm:ss+zz:zz)
- `code`: Must not exceed 1024 characters
- `uri`: Valid URI format
- `Reference`: Must be valid relative or absolute URL
- `Coding`: system + code pair

### Cardinality
- `0..1`: Optional, max one
- `1..1`: Required, exactly one
- `0..*`: Optional, multiple allowed
- `1..*: Required, at least one

## Validation Error Examples

Missing resourceType:
```json
{"name": [{"family": "Smith"}]}
// Error: resourceType is required
```

Invalid status:
```json
{"resourceType": "Encounter", "status": "open"}
// Error: 'open' is not a valid EncounterStatus code
```

Wrong data type:
```json
{"resourceType": "Patient", "birthDate": "January 15, 1990"}
// Error: birthDate must be YYYY-MM-DD format
```

Missing required reference:
```json
{"resourceType": "Observation", "status": "final", "code": {"text": "test"}}
// Error: subject is required
```

## Best Practices

1. Always include `resourceType` as the first element
2. Use proper FHIR datatypes (HumanName, ContactPoint, Address)
3. Include `meta.profile` when conforming to a profile
4. Use SNOMED CT, LOINC, or ICD codes when available
5. Include `text` for human-readable display
6. Use `identifier` for business identifiers
7. Validate before sending to a FHIR server
