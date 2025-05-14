import httpx
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
    url = f"{JiraConfig.BASE_URL}/rest/api/2/issue/{issue_id_or_key}"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {JiraConfig.API_TOKEN}"
    }
    
    # If you have a cookie for session authentication, add it here
    cookies = {}
    if hasattr(JiraConfig, 'SESSION_COOKIE') and JiraConfig.SESSION_COOKIE:
        cookies = {"JSESSIONID": JiraConfig.SESSION_COOKIE}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers=headers,
            cookies=cookies
        )
        response.raise_for_status()
        json_response = response.json()
        print(json.dumps(json_response, sort_keys=True, indent=4, separators=(",", ": ")))
        return json_response