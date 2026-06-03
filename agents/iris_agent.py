import json
import requests
from services.llm_service import get_llm
from services.iris_service import iris_service


def iris_node(state):

    question = state["question"]
    context = state.get("context", "")

    prompt = f"""
You are a FHIR assistant with IRIS server access.
Parse the user's request and determine what IRIS operation to perform.

Available operations:
- search: Search for resources (e.g., "find all patients", "search conditions for patient 123")
- read: Get a specific resource by ID (e.g., "get patient 123", "fetch encounter 456")
- create: Create a new resource from JSON (e.g., create a patient with this data: ...)
- delete: Delete a resource (e.g., "delete patient 123")

For search operations, use proper FHIR search parameters:
- Diabetes: code=http://snomed.info/sct|44054006
- Hypertension: code=http://snomed.info/sct|59621000
- Patient by name: name=xxx

User request: {question}

FHIR reference context:
{context}

Return ONLY a JSON object with these fields (no markdown, no code blocks):
- operation: search|read|create|delete
- resource_type: The FHIR resource type (Patient, Encounter, Condition, Observation, etc.)
- resource_id: The resource ID (for read/delete operations, null otherwise)
- params: Dict of search parameters (for search operations, empty dict otherwise)
- data: The resource JSON (for create operations, null otherwise)

Return raw JSON only, no explanation, no markdown.
"""

    try:
        parsed_text = get_llm().invoke(prompt).content

        # Extract JSON from response (handle markdown code blocks)
        # Remove ```json and ``` if present
        if '```' in parsed_text:
            parsed_text = parsed_text.replace('```json', '').replace('```', '').strip()

        json_start = parsed_text.find('{')
        json_end = parsed_text.rfind('}') + 1
        if json_start == -1:
            state["result"] = f"Could not parse IRIS operation from: {parsed_text}"
            return state

        parsed = json.loads(parsed_text[json_start:json_end])

        operation = parsed.get("operation", "search")
        resource_type = parsed.get("resource_type", "Patient")
        resource_id = parsed.get("resource_id")
        params = parsed.get("params", {})
        data = parsed.get("data")

        if operation == "search":
            result = iris_service.search_resource(resource_type, params)
            # Format the search results
            entries = result.get("entry", [])
            total = result.get("total", len(entries))
            output = f"Found {total} {resource_type} resource(s):\n\n"
            for entry in entries[:5]:  # Show first 5
                resource = entry.get("resource", {})
                # Extract key info for display
                name = resource.get("name", [{}])[0] if resource.get("name") else {}
                display_name = f"{name.get('given', [''])[0]} {name.get('family', '')}"
                gender = resource.get("gender", "unknown")
                birth_date = resource.get("birthDate", "N/A")
                output += f"ID: {resource.get('id')} | {display_name.strip()} | {gender} | {birth_date}\n"
            if total > 5:
                output += f"\n... and {total - 5} more results"
            state["result"] = output

        elif operation == "read":
            if not resource_id:
                state["result"] = "Error: resource_id is required for read operation"
                return state
            result = iris_service.get_resource(resource_type, resource_id)
            state["result"] = f"Resource {resource_type}/{resource_id}:\n\n" + json.dumps(result, indent=2)

        elif operation == "create":
            if not data:
                state["result"] = "Error: data is required for create operation"
                return state
            # data should be a dict, convert to JSON string if needed
            data_str = json.dumps(data) if isinstance(data, dict) else data
            result = iris_service.create_resource(resource_type, data_str)
            state["result"] = f"Created {resource_type}:\n\n" + json.dumps(result, indent=2)

        elif operation == "delete":
            if not resource_id:
                state["result"] = "Error: resource_id is required for delete operation"
                return state
            result = iris_service.delete_resource(resource_type, resource_id)
            state["result"] = f"Deleted {resource_type}/{resource_id}"
        else:
            state["result"] = f"Unknown operation: {operation}"

    except requests.exceptions.HTTPError as e:
        # Try to parse OperationOutcome
        try:
            outcome = e.response.json()
            issues = outcome.get("issue", [])
            if issues:
                diag = issues[0].get("diagnostics", e.response.text)
                state["result"] = f"IRIS error: {diag}"
            else:
                state["result"] = f"IRIS API error: {e.response.status_code} - {e.response.text}"
        except Exception:
            state["result"] = f"IRIS API error: {e.response.status_code} - {e.response.text}"
    except requests.exceptions.ConnectionError:
        state["result"] = "Cannot connect to IRIS server. Please check if IRIS is running."
    except json.JSONDecodeError as e:
        state["result"] = f"Failed to parse response: {str(e)}"
    except Exception as e:
        state["result"] = f"IRIS operation failed: {str(e)}"

    return state
