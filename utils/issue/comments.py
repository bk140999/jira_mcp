import httpx
from typing import Dict, Any, List
from ..config import JiraConfig
import json

async def get_comments(issue_key: str) -> Dict[str, Any]:
    """
    Get all comments for a Jira issue.
    
    Args:
        issue_key: The key of the issue to get comments for
        
    Returns:
        Dict containing the comments
    """
    JiraConfig.validate_config()
    url = f"{JiraConfig.BASE_URL}/rest/api/2/issue/{issue_key}/comment"
    
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
                "comments": json_response
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

async def add_comment(issue_key: str, comment: str) -> Dict[str, Any]:
    """
    Add a comment to a Jira issue.
    
    Args:
        issue_key: The key of the issue to add comment to
        comment: The comment text to add
        
    Returns:
        Dict containing the response from Jira
    """
    JiraConfig.validate_config()
    url = f"{JiraConfig.BASE_URL}/rest/api/2/issue/{issue_key}/comment"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {JiraConfig.API_TOKEN}"
    }
    
    # If you have a cookie for session authentication, add it here
    cookies = {}
    if hasattr(JiraConfig, 'SESSION_COOKIE') and JiraConfig.SESSION_COOKIE:
        cookies = {"JSESSIONID": JiraConfig.SESSION_COOKIE}

    payload = {
        "body": comment
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=payload,
                headers=headers,
                cookies=cookies
            )
            response.raise_for_status()
            json_response = response.json()
            return {
                "success": True,
                "response": json_response
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