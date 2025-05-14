import httpx
from typing import Dict, Any
from ..config import JiraConfig

async def search_issues(jql: str, max_results: int = 50) -> Dict[str, Any]:
    """
    Search Jira issues using JQL.
    
    Args:
        jql: The JQL query string
        max_results: Maximum number of results to return (default 50)
        
    Returns:
        Dict containing the matching issues
    """
    JiraConfig.validate_config()
    url = f"{JiraConfig.BASE_URL}/rest/api/2/search"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {JiraConfig.API_TOKEN}"
    }
    
    # If you have a cookie for session authentication, add it here
    cookies = {}
    if hasattr(JiraConfig, 'SESSION_COOKIE') and JiraConfig.SESSION_COOKIE:
        cookies = {"JSESSIONID": JiraConfig.SESSION_COOKIE}

    params = {
        "jql": jql,
        "maxResults": max_results
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers=headers,
                cookies=cookies,
                params=params
            )
            response.raise_for_status()
            json_response = response.json()
            return {
                "success": True,
                "issues": json_response
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