import json
import requests
from services.llm_service import get_llm
from services.iris_service import iris_service


def query_node(state):

    question = state["question"]
    context = state.get("context", "")

    prompt = f"""
Convert natural language to FHIR Search API.

Use the following FHIR Search reference:
{context}

Question: {question}

Return ONLY the search URL path and parameters, for example:
Patient?name=Smith
Condition?code=http://snomed.info/sct|44054006
Observation?patient=Patient/123&category=laboratory

Do NOT include the base URL. Return the path only.
"""

    search_query = get_llm().invoke(prompt).content.strip()

    # Clean up the response - remove any markdown or extra text
    if '```' in search_query:
        search_query = search_query.replace('```', '').strip()
    # Extract just the path (ResourceType?params)
    lines = search_query.split('\n')
    for line in lines:
        line = line.strip()
        if '?' in line and '/' not in line.split('?')[0]:
            search_query = line
            break

    # Try to execute the query against IRIS
    try:
        # Split into resource type and params
        parts = search_query.split('?', 1)
        resource_type = parts[0].strip()
        params_str = parts[1].strip() if len(parts) > 1 else ''

        # Parse params into dict
        params = {}
        if params_str:
            for param in params_str.split('&'):
                if '=' in param:
                    key, value = param.split('=', 1)
                    params[key] = value

        # Execute search
        result = iris_service.search_resource(resource_type, params)

        # If no results with code, try common diabetes codes
        if result.get("total", 0) == 0 and "code" in params:
            code_value = params["code"]
            if "73211009" in code_value:  # Generic diabetes code
                # Try Type 2 diabetes
                params["code"] = "http://snomed.info/sct|44054006"
                result = iris_service.search_resource(resource_type, params)

        # Format results
        entries = result.get("entry", [])
        total = result.get("total", len(entries))

        # Build full URL with auth for browser access
        full_url = iris_service.get_browser_url(search_query)
        output = f"FHIR Search: {full_url}\n\n"
        output += f"Found {total} result(s):\n\n"

        # Collect full resources for JSON display
        full_resources = []

        for entry in entries[:10]:  # Show first 10
            resource = entry.get("resource", {})
            rt = resource.get("resourceType", "Unknown")

            # Skip OperationOutcome errors
            if rt == "OperationOutcome":
                continue

            # Store full resource for JSON display
            full_resources.append(resource)

            # Generate browser-accessible URLs with auth params
            if rt == "Patient":
                name = resource.get("name", [{}])[0]
                display = f"{name.get('given', [''])[0]} {name.get('family', '')}"
                gender = resource.get("gender", "N/A")
                birth = resource.get("birthDate", "N/A")
                url = iris_service.get_browser_url(f"Patient/{resource.get('id')}")
                output += f"[{rt}] {url}\n"
                output += f"  Name: {display.strip()} | Gender: {gender} | Birth: {birth}\n\n"

            elif rt == "Condition":
                code = resource.get("code", {}).get("coding", [{}])[0]
                display = code.get("display", "N/A")
                patient_ref = resource.get("subject", {}).get("reference", "N/A")
                onset = resource.get("onsetDateTime", "N/A")[:10]
                url = iris_service.get_browser_url(f"Condition/{resource.get('id')}")
                output += f"[{rt}] {url}\n"
                output += f"  {display} | Patient: {patient_ref} | Onset: {onset}\n\n"

            elif rt == "Observation":
                code = resource.get("code", {}).get("coding", [{}])[0]
                display = code.get("display", "N/A")
                patient_ref = resource.get("subject", {}).get("reference", "N/A")
                value = resource.get("valueQuantity", {})
                val_str = f"{value.get('value', '')} {value.get('unit', '')}" if value else "N/A"
                url = iris_service.get_browser_url(f"Observation/{resource.get('id')}")
                output += f"[{rt}] {url}\n"
                output += f"  {display} | Patient: {patient_ref} | Value: {val_str}\n\n"

            elif rt == "Encounter":
                patient_ref = resource.get("subject", {}).get("reference", "N/A")
                status = resource.get("status", "N/A")
                period = resource.get("period", {})
                start = period.get("start", "N/A")[:10]
                url = iris_service.get_browser_url(f"Encounter/{resource.get('id')}")
                output += f"[{rt}] {url}\n"
                output += f"  Patient: {patient_ref} | Status: {status} | Start: {start}\n\n"

            else:
                url = iris_service.get_browser_url(f"{rt}/{resource.get('id')}")
                output += f"[{rt}] {url}\n\n"

        if total > 10:
            output += f"... and {total - 10} more results\n\n"

        # Add formatted JSON output
        if full_resources:
            output += "=" * 50 + "\n"
            output += "JSON Response:\n"
            output += "=" * 50 + "\n\n"
            if len(full_resources) == 1:
                output += json.dumps(full_resources[0], indent=2, ensure_ascii=False)
            else:
                output += json.dumps(full_resources, indent=2, ensure_ascii=False)

        state["result"] = output

    except requests.exceptions.HTTPError as e:
        full_url = f"{iris_service.base_url}/{search_query}"
        state["result"] = f"FHIR Search: {full_url}\n\nIRIS error: {e.response.status_code}"
    except Exception as e:
        full_url = f"{iris_service.base_url}/{search_query}"
        state["result"] = f"FHIR Search: {full_url}\n\nQuery execution failed: {str(e)}"

    return state
