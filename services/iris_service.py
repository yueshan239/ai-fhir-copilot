import json
import base64
import requests
from config import settings


class IrisService:
    """Service for interacting with InterSystems IRIS FHIR server."""

    def _get_base_url(self):
        return f"{settings.IRIS_HOST}{settings.IRIS_FHIR_PATH}"

    def _get_auth_header(self):
        credentials = f"{settings.IRIS_USERNAME}:{settings.IRIS_PASSWORD}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded}"

    def _get_headers(self):
        return {
            "Content-Type": "application/fhir+json",
            "Accept": "application/fhir+json",
            "Authorization": self._get_auth_header(),
        }

    def get_browser_url(self, path: str) -> str:
        """Get URL for display (without auth in URL)."""
        return f"{self._get_base_url()}/{path}"

    def search_resource(self, resource_type: str, params: dict = None):
        """Search for FHIR resources."""
        response = requests.get(
            f"{self._get_base_url()}/{resource_type}",
            params=params or {},
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    def get_resource(self, resource_type: str, resource_id: str):
        """Read a FHIR resource by ID."""
        response = requests.get(
            f"{self._get_base_url()}/{resource_type}/{resource_id}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    def create_resource(self, resource_type: str, resource_json: str):
        """Create a new FHIR resource."""
        response = requests.post(
            f"{self._get_base_url()}/{resource_type}",
            data=resource_json if isinstance(resource_json, str) else json.dumps(resource_json),
            headers=self._get_headers(),
        )
        response.raise_for_status()
        # IRIS returns 201 with no body, extract ID from Location header
        if response.status_code == 201 and not response.text:
            location = response.headers.get("Location", "")
            # Extract ID from URL like http://host/fhir/r4/Patient/123/_history/1
            parts = location.rstrip("/").split("/")
            resource_id = parts[-3] if len(parts) >= 4 else "unknown"
            return {
                "resourceType": resource_type,
                "id": resource_id,
                "created": True,
                "location": location,
            }
        return response.json()

    def update_resource(self, resource_type: str, resource_id: str, resource_json: str):
        """Update an existing FHIR resource."""
        response = requests.put(
            f"{self._get_base_url()}/{resource_type}/{resource_id}",
            data=resource_json if isinstance(resource_json, str) else json.dumps(resource_json),
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    def delete_resource(self, resource_type: str, resource_id: str):
        """Delete a FHIR resource."""
        response = requests.delete(
            f"{self._get_base_url()}/{resource_type}/{resource_id}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return {"deleted": True, "id": resource_id}

    def execute_bundle(self, bundle_json: str):
        """Execute a FHIR transaction bundle."""
        response = requests.post(
            self._get_base_url(),
            data=bundle_json if isinstance(bundle_json, str) else json.dumps(bundle_json),
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()


iris_service = IrisService()
