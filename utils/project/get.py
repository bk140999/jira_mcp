import httpx
from httpx import BasicAuth
from typing import Dict, Any, Optional
from ..config import JiraConfig

async def get_project(project_key: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Get a single Jira project by ID or key.
    
    Args:
        project_key: The ID or key of the project to retrieve
        project_key: The key of the project to retrieve
    Returns:
        Dict containing the project details
    """
    JiraConfig.validate_config()
    if project_key:
        url = f"{JiraConfig.BASE_URL}/rest/api/3/project/{project_key}"
    elif project_id:
        url = f"{JiraConfig.BASE_URL}/rest/api/3/project/{project_id}"
    else:
        raise ValueError("Either project_key or project_id must be provided")
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
        print(json_response)
        return json_response

