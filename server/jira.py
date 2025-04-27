from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import os
from utils.issue.create import create_jira_ticket
from utils.project.get_all import get_all_projects
from utils.project.get import get_project
from utils.issue.get import get_issue
from typing import Optional
from utils.config import JiraConfig

mcp = FastMCP("Jira")

@mcp.tool()
async def create_jira_ticket_tool(
    issue_type: str,
    summary: str,
    description: str,
    project_id: str,
    reporter_id: str = JiraConfig.USER_ID,
    parent_key: str = None,
    labels: list = None,
    security_id: str = None,
    original_estimate: str = None,
    remaining_estimate: str = None,
    versions: list = None
) -> None:
    return await create_jira_ticket(
        summary=summary,
        description=description,
        project_id=project_id,
        issue_type_name=issue_type,
        reporter_id=reporter_id,
        parent_key=parent_key,
        labels=labels,
        security_id=security_id,
        original_estimate=original_estimate,
        remaining_estimate=remaining_estimate,
        versions=versions
    )

@mcp.tool()
async def get_project_by_id_tool(project_id: str) -> Any:
    return await get_project(project_id=project_id)

@mcp.tool()
async def get_project_by_key_tool(project_key: str) -> Any:
    return await get_project(project_key=project_key)

@mcp.tool()
async def get_multiple_projects_tool():
    return await get_all_projects()

@mcp.tool()
async def get_issue_tool(issue_key: str):
    return await get_issue(issue_key)

if __name__ == "__main__":
    print("Starting server")
    # Initialize and run the server
    mcp.run()
    print("Server is running")
