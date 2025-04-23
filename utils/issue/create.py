import os
import json
import httpx
from httpx import BasicAuth
from typing import Dict, Any, Optional, List
from ..config import JiraConfig

async def create_jira_ticket(
    summary: str,
    description: str,
    project_id: str,
    issue_type_name: Optional[str] = "Task",
    reporter_id: Optional[str] = None,
    assignee_id: Optional[str] = None,
    components: Optional[List[str]] = None,
    parent_key: Optional[str] = None,
    labels: Optional[List[str]] = None,
    security_id: Optional[str] = None,
    original_estimate: Optional[str] = None,
    remaining_estimate: Optional[str] = None,
    versions: Optional[List[str]] = None,
    fix_versions: Optional[List[str]] = None,
    due_date: Optional[str] = None,
    environment: Optional[str] = None
) -> None:
    JiraConfig.validate_config()
    url = JiraConfig.BASE_URL + "/rest/api/3/issue"
    auth = BasicAuth(JiraConfig.USER_EMAIL, JiraConfig.API_TOKEN)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    fields: Dict[str, Any] = {
        "issuetype": {"name": issue_type_name},
        "summary": summary,
        "description": {
            "content": [
                {
                    "content": [
                        {
                            "text": description,
                            "type": "text"
                        }
                    ],
                    "type": "paragraph"
                }
            ],
            "type": "doc",
            "version": 1
        },
        "project": {"id": project_id},
    }

    if assignee_id:
        fields["assignee"] = {"id": assignee_id}
    if components:
        fields["components"] = [{"id": comp_id} for comp_id in components]
    if parent_key:
        fields["parent"] = {"key": parent_key}
    if labels:
        fields["labels"] = labels
    if security_id:
        fields["security"] = {"id": security_id}
    if original_estimate or remaining_estimate:
        fields["timetracking"] = {
            "originalEstimate": original_estimate,
            "remainingEstimate": remaining_estimate
        }
    if versions:
        fields["versions"] = [{"id": version_id} for version_id in versions]
    if fix_versions:
        fields["fixVersions"] = [{"id": version_id} for version_id in fix_versions]
    if due_date:
        fields["duedate"] = due_date
    if environment:
        fields["environment"] = {
            "content": [
                {
                    "content": [
                        {
                            "text": environment,
                            "type": "text"
                        }
                    ],
                    "type": "paragraph"
                }
            ],
            "type": "doc",
            "version": 1
        }

    payload = {
        "fields": fields,
        "update": {}
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json=payload,
            headers=headers,
            auth=auth
        )
        # print("API call is done")
        # print(json.dumps(response.json(), sort_keys=True, indent=4, separators=(",", ": ")))
        return response.json()