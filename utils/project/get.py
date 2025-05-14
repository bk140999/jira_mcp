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
        url = f"{JiraConfig.BASE_URL}/rest/api/2/project/{project_key}"
    elif project_id:
        url = f"{JiraConfig.BASE_URL}/rest/api/2/project/{project_id}"
    else:
        raise ValueError("Either project_key or project_id must be provided")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {JiraConfig.API_TOKEN}"
    }
    
    # If you have a cookie for session authentication, add it here
    cookies = {}
    if hasattr(JiraConfig, 'SESSION_COOKIE') and JiraConfig.SESSION_COOKIE:
        cookies = {"JSESSIONID": JiraConfig.SESSION_COOKIE}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers=headers,
                cookies=cookies
            )
            response.raise_for_status()
            json_response = response.json()
            return {
                "success": True,
                "project": json_response
            }
    except httpx.HTTPStatusError as e:
        return {
            "success": False,
            "error": f"HTTP error occurred: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"An error occurred: {str(e)}"
        }

