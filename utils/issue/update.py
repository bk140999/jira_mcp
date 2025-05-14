import json
import httpx
from typing import Dict, Any, Optional, List
from ..config import JiraConfig

async def update_jira_ticket(
    issue_key: str,
    summary: str = None,
    description: str = None,
    status_name: str = None,
    priority: str = None,
    assignee: str = None,
    fin_business_cost_center: List[str] = None,
    flows: str = None,
    tag_types: str = None,
    beat_types: str = None,
) -> Dict[str, Any]:
    """
    Update a Jira ticket with the given parameters
    Args:
        issue_key: Key of the ticket to update (e.g., 'FCA-1234')
        summary: Updated title of the ticket
        description: Updated description of the ticket
        status_name (str): The **name** of the status to transition the ticket to (e.g., "In Progress", "Closed")
        priority: Updated priority of the ticket
        assignee: Updated username of the assignee
        fin_business_cost_center: Updated list of Fin_Business Cost Center values (customfield_19805)
        flows: Updated Flows value (customfield_20408)
        tag_types: Updated Tag Types value (customfield_20411)
        beat_types: Updated Beat Types value (customfield_20409)
    Returns:
        Dict containing the response from Jira
    """
    JiraConfig.validate_config()
    url = f"{JiraConfig.BASE_URL}/rest/api/2/issue/{issue_key}"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {JiraConfig.API_TOKEN}",
    }

    # Add cookie if configured
    if hasattr(JiraConfig, 'COOKIE') and JiraConfig.COOKIE:
        headers["Cookie"] = JiraConfig.COOKIE

    # Create fields object with only the fields that need to be updated
    fields = {}
    
    if summary is not None:
        fields["summary"] = summary
    if description is not None:
        fields["description"] = description
    
    if priority is not None:
        fields["priority"] = {"name": priority}
    
    if assignee is not None:
        fields["assignee"] = {"name": assignee}
    
    if fin_business_cost_center is not None:
        fields["customfield_19805"] = [{"value": str(value)} for value in fin_business_cost_center]
    
    if flows is not None:
        fields["customfield_20408"] = flows
    
    if tag_types is not None:
        fields["customfield_20411"] = tag_types
    
    if beat_types is not None:
        fields["customfield_20409"] = beat_types

    payload = {"fields": fields}

    # If status needs to be updated, we need to make a transition request
    if status_name is not None:
        async with httpx.AsyncClient() as client:
            transitions_response = await client.get(
                f"{url}/transitions?expand=transitions.fields",
                headers=headers
            )
            transitions_response.raise_for_status()
            transitions = transitions_response.json()["transitions"]

            print(f"Available transitions: {json.dumps(transitions, indent=2)}")

            transition_id = None
            transition_fields_required = {}

            for transition in transitions:
                if transition["to"]["name"].lower() == status_name.lower():
                    transition_id = transition["id"]
                    transition_fields_required = transition.get("fields", {})
                    break

            if transition_id:
                transition_payload = {
                    "transition": {
                        "id": transition_id
                    }
                }

                # Optional: Add resolution if required
                if "resolution" in transition_fields_required:
                    transition_payload["fields"] = {
                        "resolution": {"name": "Done"}  # Or another value depending on workflow
                    }

                print("Sending transition payload:", json.dumps(transition_payload, indent=2))

                transition_resp = await client.post(
                    f"{url}/transitions",
                    json=transition_payload,
                    headers=headers
                )
                transition_resp.raise_for_status()

    # Update other fields
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                url,
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            
            return {
                "isIssueUpdated": True,
                "response": "Successfully updated"
            }
    except httpx.HTTPStatusError as e:
        return {
            "isIssueUpdated": False,
            "error": f"HTTP error occurred: {str(e)}\nResponse: {e.response.text if hasattr(e, 'response') else 'No response text'}"
        }
    except Exception as e:
        return {
            "isIssueUpdated": False,
            "error": f"An error occurred: {str(e)}"
        } 