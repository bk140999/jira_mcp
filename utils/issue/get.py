import httpx
from httpx import BasicAuth 
from typing import Dict, Any
from ..config import JiraConfig
import json
async def get_issue(issue_id_or_key: str) -> Dict[str, Any]:
    """
    Get a single Jira issue by ID or key.
    
    Args:
        issue_id_or_key: The ID or key of the issue to retrieve
        
    Returns:
        Dict containing the issue details
    """
    JiraConfig.validate_config()
    url = f"{JiraConfig.BASE_URL}/rest/api/3/issue/{issue_id_or_key}"
    auth = BasicAuth(JiraConfig.USER_EMAIL, JiraConfig.API_TOKEN)
    headers = {
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers=headers,
            auth=auth
        )
        response.raise_for_status()
        json_response = response.json()
        print(json.dumps(json_response, sort_keys=True, indent=4, separators=(",", ": ")))
        return json_response