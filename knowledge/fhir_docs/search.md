# FHIR Search API Reference

FHIR Search provides a standard mechanism for searching FHIR resources. It supports RESTful queries with query parameters.

## Common Search Parameters

All resources support these standard parameters:
- `_id`: Logical id of the resource
- `_lastUpdated`: When the resource version last changed
- `_tag`: Search by tag
- `_profile`: Search by profile
- `_security`: Search by security labels

## Parameter Types

### String
Searches string fields. Supports `:contains` and `:exact` modifiers.
```
GET /Patient?name=Smith
GET /Patient?name:contains=john
GET /Patient?name:exact=John Smith
```

### Token
Searches coded values (system|code format).
```
GET /Patient?gender=male
GET /Condition?code=http://snomed.info/sct|44054006
GET /Observation?code=85354-9
```

### Reference
Searches references to other resources.
```
GET /Encounter?patient=Patient/123
GET /Condition?subject=Patient/123
```

### Date
Searches date/dateTime fields. Supports prefixes: eq, ne, lt, gt, le, ge.
```
GET /Observation?date=2024-01-15
GET /Encounter?date=ge2024-01-01&date=le2024-01-31
GET /Patient?birthdate=ge1990-01-01
```

### Number
Searches numeric fields.
```
GET /Observation?value-quantity=gt100
```

### Quantity
Searches quantity values with units.
```
GET /Observation?value-quantity=gt100||mmHg
```

### Composite
Combines multiple parameters.
```
GET /Observation?code-value-quantity=http://loinc.org|2339-0||gt200
```

## Result Modifiers

- `_count`: Limit number of results per page
- `_offset`: Skip results for pagination
- `_sort`: Sort results (prefix `-` for descending)
- `_include`: Include referenced resources
- `_revinclude`: Include resources that reference this one
- `_summary`: Return only summary (true, text, data)
- `_elements`: Return only specific elements

## Chained Parameters

Search through references:
```
GET /Condition?patient.name=Smith
GET /Observation?subject:Patient.name=Smith
```

## Examples

Find diabetic patients:
```
GET /Condition?code=http://snomed.info/sct|44054006&_include=Condition:subject
```

Find recent lab results for a patient:
```
GET /Observation?patient=Patient/123&category=laboratory&date=ge2024-01-01&_sort=-date
```

Find active conditions:
```
GET /Condition?patient=Patient/123&clinical-status=active
```

Find encounters in date range:
```
GET /Encounter?patient=Patient/123&date=ge2024-01-01&date=le2024-12-31
```

Search with pagination:
```
GET /Patient?_count=10&_offset=0
```
