import os
import json
import httpx
from typing import Dict, Any, Optional, List
from ..config import JiraConfig

async def create_jira_ticket(
    summary: str,
    description: str,
    project_id: str = "20648",
    issue_type: str = "1",  # Default to Bug type
    priority: Optional[str] = None,
    assignee: Optional[str] = None,
    fin_business_cost_center: List[str] = ["EDC & Enterprise"],  # Default value for customfield_19805
    flows: str = "*",  # Default value for customfield_20408
    tag_types: str = "*",  # Default value for customfield_20411
    beat_types: str = "*",  # Default value for customfield_20409
    # reporter: Optional[str] = None,
    # custom_fields: Optional[Dict[str, Any]] = None,
    # parent_key: Optional[str] = None,
    # labels: Optional[List[str]] = None,
    # security_id: Optional[str] = None,
    # original_estimate: Optional[str] = None,
    # remaining_estimate: Optional[str] = None,
    # versions: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Create a Jira ticket with the given parameters
    Args:
        summary: Title of the ticket
        description: Description of the ticket
        project_id: ID of the project
        issue_type: Type of issue (default is "1" for Bug)
        priority: Priority of the ticket
        assignee: Username of the assignee
        fin_business_cost_center: List of Fin_Business Cost Center values (customfield_19805)
        flows: Flows value (customfield_20408)
        tag_types: Tag Types value (customfield_20411)
        beat_types: Beat Types value (customfield_20409)
    Returns:
        Dict containing the response from Jira
    """
    JiraConfig.validate_config()
    url = JiraConfig.BASE_URL + "/rest/api/2/issue"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {JiraConfig.API_TOKEN}",
    }

    # Add cookie if configured
    if hasattr(JiraConfig, 'COOKIE') and JiraConfig.COOKIE:
        headers["Cookie"] = JiraConfig.COOKIE

    # Create fields object similar to Java implementation
    fields = {
        "project": { "id": project_id },  # Changed from key to id
        "issuetype": { "id": issue_type },  # Changed from name to id
        "summary": summary,
        "description": description,
        # Add required custom fields with default values
        "customfield_19805": [{"value": str(value)} for value in fin_business_cost_center],  # Fin_Business Cost Center
        "customfield_20408": flows,  # Flows
        "customfield_20411": tag_types,  # Tag Types
        "customfield_20409": beat_types,  # Beat Types
    }

    # Add priority if specified
    if priority:
        fields["priority"] = {"name": priority}

    # Add assignee if specified
    if assignee:
        fields["assignee"] = {"name": assignee}

    # Add reporter if specified
    # if reporter:
    #     fields["reporter"] = {"name": reporter}

    # # Add security if specified
    # if security_id:
    #     fields["security"] = {"id": security_id}

    # # Add labels if specified
    # if labels:
    #     fields["labels"] = labels

    # # Add versions if specified
    # if versions:
    #     fields["versions"] = [{"name": version} for version in versions]

    # # Add parent if specified
    # if parent_key:
    #     fields["parent"] = {"key": parent_key}

    # # Add estimates if specified
    # if original_estimate:
    #     fields["timetracking"] = {"originalEstimate": original_estimate}
    #     if remaining_estimate:
    #         fields["timetracking"]["remainingEstimate"] = remaining_estimate

    # # Add custom fields if provided
    # if custom_fields:
    #     fields.update(custom_fields)

    payload = {"fields": fields}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            result = response.json()
            
            return {
                "isIssueLogged": True,
                "response": result
            }
    except httpx.HTTPStatusError as e:
        return {
            "isIssueLogged": False,
            "error": f"HTTP error occurred: {str(e)}\nResponse: {e.response.text if hasattr(e, 'response') else 'No response text'}"
        }
    except Exception as e:
        return {
            "isIssueLogged": False,
            "error": f"An error occurred: {str(e)}"
        }