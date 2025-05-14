from typing import Any, Dict, List
from dotenv import load_dotenv
import httpx
import json
import os
from mcp.server.fastmcp import FastMCP
from utils.issue.create import create_jira_ticket
from utils.project.get_all import get_all_projects
from utils.project.get import get_project
from utils.issue.get import get_issue
from utils.issue.comments import get_comments, add_comment
from utils.issue.search import search_issues
from typing import Optional
from utils.config import JiraConfig
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from mcp.server.fastmcp.server import Settings, Context
from sse_starlette.sse import ServerSentEvent
from mcp.server.sse import SseServerTransport
from pydantic_settings import BaseSettings
from starlette.responses import JSONResponse

# Load environment variables
load_dotenv()

# Load MCP configuration from JSON
with open('jira-mcp.json', 'r') as config_file:
    mcp_config = json.load(config_file)

# Get server configuration
SERVER_HOST = mcp_config['server']['host']
SERVER_PORT = 7777  # Use a completely new port

# Initialize FastMCP settings
settings = Settings(port=SERVER_PORT, debug=False)

# Initialize FastMCP with configuration from JSON
mcp = FastMCP(
    mcp_config['name'],
    host=SERVER_HOST,
    port=SERVER_PORT
)

@mcp.tool()
async def create_jira_ticket_tool(
    issue_type: str = "1",
    summary: str = "",
    description: str = "",
    project_id: str = "31900",  # Default project ID from Java code
    priority: str = "Medium",
    assignee: str = None,
    fin_business_cost_center: List[str] = ["EDC & Enterprise"],  # Default value for customfield_19805
    flows: str = "*",
    tag_types: str = "*",
    beat_types: str = "*",
) -> None:
    """
    Create a Jira ticket with specified parameters.

    Args:
        issue_type (str, optional): The type of issue to create. Defaults to "1" (typically represents a Task).
        summary (str): The title or summary of the Jira ticket.
        description (str): Detailed description of the issue.
        project_id (str, optional): The ID of the project where the ticket will be created. Defaults to "31900".
        priority (str, optional): Priority level of the ticket. Defaults to "Medium".
        assignee (str, optional): Username of the person to whom the ticket should be assigned. Defaults to None.
        fin_business_cost_center (List[str], optional): Financial business cost center for the ticket. 
            Defaults to ["EDC & Enterprise"].
        flows (str, optional): Workflow flows associated with the ticket. Defaults to "*".
        tag_types (str, optional): Types of tags to be associated with the ticket. Defaults to "*".
        beat_types (str, optional): Types of beats related to the ticket. Defaults to "*".

    Returns:
        None: The function returns the result of create_jira_ticket function call.

    Example:
        >>> await create_jira_ticket_tool(
        ...     summary="Fix login bug",
        ...     description="Users unable to login using SSO",
        ...     priority="High",
        ...     assignee="john.doe"
        ... )
    """
    return await create_jira_ticket(
        summary=summary,
        description=description,
        project_id=project_id,
        issue_type=issue_type,
        priority=priority,
        assignee=assignee,
        fin_business_cost_center=fin_business_cost_center,
        flows=flows,
        tag_types=tag_types,
        beat_types=beat_types,
    )

@mcp.tool()
async def get_project_by_id_tool(project_id: str) -> Any:
    """
    Retrieve project details using the project ID.

    Args:
        project_id (str): The unique identifier of the Jira project.

    Returns:
        Any: Project details including name, key, lead, and other metadata.

    Example:
        >>> await get_project_by_id_tool(project_id="31900")
    """
    return await get_project(project_id=project_id)

@mcp.tool()
async def get_project_by_key_tool(project_key: str) -> Any:
    """
    Retrieve project details using the project key.

    Args:
        project_key (str): The project key (e.g., 'FCA', 'PROJ', etc.).

    Returns:
        Any: Project details including name, ID, lead, and other metadata.

    Example:
        >>> await get_project_by_key_tool(project_key="FCA")
    """
    return await get_project(project_key=project_key)

@mcp.tool()
async def get_multiple_projects_tool(random_string: str):
    """
    Retrieve details of all accessible Jira projects.

    Args:
        random_string (str): A placeholder parameter required by the tool framework.

    Returns:
        List[Dict]: A list of dictionaries containing details of all projects.
            Each dictionary contains project information like ID, key, name, etc.

    Example:
        >>> await get_multiple_projects_tool(random_string="dummy")
    """
    return await get_all_projects()

@mcp.tool()
async def get_issue_tool(issue_key: str):
    """
    Retrieve detailed information about a specific Jira issue.

    Args:
        issue_key (str): The unique key of the issue (e.g., 'FCA-1234').

    Returns:
        Dict: Complete issue details including summary, description, status,
            assignee, reporter, comments, and custom fields.

    Example:
        >>> await get_issue_tool(issue_key="FCA-1234")
    """
    return await get_issue(issue_key)

@mcp.tool()
async def get_comments_tool(issue_key: str) -> Dict[str, Any]:
    """
    Retrieve all comments associated with a Jira issue.

    Args:
        issue_key (str): The unique key of the issue (e.g., 'FCA-1234').

    Returns:
        Dict[str, Any]: A dictionary containing:
            - comments: List of all comments with author, content, and timestamp
            - error: Error information if the request fails
            - success: Boolean indicating if the request was successful

    Example:
        >>> await get_comments_tool(issue_key="FCA-1234")
    """
    return await get_comments(issue_key)

@mcp.tool()
async def add_comment_tool(issue_key: str, comment: str) -> Dict[str, Any]:
    """
    Add a new comment to an existing Jira issue.

    Args:
        issue_key (str): The unique key of the issue (e.g., 'FCA-1234').
        comment (str): The text content of the comment to be added.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - response: Comment creation confirmation details
            - error: Error information if the comment creation fails
            - success: Boolean indicating if the comment was added successfully

    Example:
        >>> await add_comment_tool(
        ...     issue_key="FCA-1234",
        ...     comment="Implementation completed, ready for review."
        ... )
    """
    return await add_comment(issue_key, comment)

@mcp.tool()
async def search_issues_tool(
    project_key: str = "FCA",
    assignee: str = JiraConfig.USER_ID,
    reporter: str = None,
    fixVersion: str = None,
    dev_assignee: str = None,
    qa_assignee: str = None,
    max_results: int = 5,
    be_delivery_date: str = None,
    fe_delivery_date: str = None,
    dev_delivery_date: str = None,
    qa_delivery_date: str = None,
    qa_required: str = None,
    dependent_systems: str = None,
    epic_link: str = None,
    sprint: str = None,
    priority: str = None,
    issue_type: str = None,
    status: List[str] = None,
) -> Dict[str, Any]:
    """
    Search for Jira issues using various filters and criteria.

    Args:
        project_key (str, optional): The project key to search in. Defaults to "FCA".
        assignee (str, optional): Username of the assignee to filter by. Defaults to current user.
        reporter (str, optional): Username of the issue reporter. Defaults to None.
        fixVersion (str, optional): Version where the issue is planned to be fixed. Defaults to None.
        dev_assignee (str, optional): Developer assigned to the issue. Defaults to None.
        qa_assignee (str, optional): QA person assigned to the issue. Defaults to None.
        max_results (int, optional): Maximum number of issues to return. Defaults to 5.
        be_delivery_date (str, optional): Backend delivery date (customfield_20109). Defaults to None.
        fe_delivery_date (str, optional): Frontend delivery date (customfield_20108). Defaults to None.
        dev_delivery_date (str, optional): Development delivery date (customfield_19204). Defaults to None.
        qa_delivery_date (str, optional): QA delivery date (customfield_19205). Defaults to None.
        qa_required (str, optional): Whether QA is required (customfield_13303). Defaults to None.
        dependent_systems (str, optional): Related dependent systems (customfield_15506). Defaults to None.
        epic_link (str, optional): Link to the epic (customfield_10008). Defaults to None.
        sprint (str, optional): Sprint name or ID (customfield_10007). Defaults to None.
        priority (str, optional): Issue priority level. Defaults to None.
        issue_type (str, optional): Type of the issue. Defaults to None.
        status (List[str], optional): List of issue statuses to filter by. Defaults to None.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - issues: List of matching issues with their details
            - total: Total number of matching issues
            - success: Boolean indicating if the search was successful
            - error: Error information if the search fails

    Example:
        >>> await search_issues_tool(
        ...     project_key="FCA",
        ...     assignee="john.doe",
        ...     priority="High",
        ...     status=["In Progress", "To Do"],
        ...     max_results=10
        ... )
    """
    jql_conditions = [f"project = {project_key}"]
    
    if assignee and assignee.lower() != 'null':
        jql_conditions.append(f"assignee = {assignee}")
    if reporter:
        jql_conditions.append(f"reporter = {reporter}")
    if fixVersion:
        jql_conditions.append(f'fixVersion = "{fixVersion}"')
    if dev_assignee:
        jql_conditions.append(f'"Dev Assignee" = "{dev_assignee}"')
    if qa_assignee:
        jql_conditions.append(f'"QA Assignee" = "{qa_assignee}"')
    if be_delivery_date:
        jql_conditions.append(f'cf[20109] = "{be_delivery_date}"')
    if fe_delivery_date:
        jql_conditions.append(f'cf[20108] = "{fe_delivery_date}"')
    if dev_delivery_date:
        jql_conditions.append(f'cf[19204] = "{dev_delivery_date}"')
    if qa_delivery_date:
        jql_conditions.append(f'cf[19205] = "{qa_delivery_date}"')
    if qa_required:
        jql_conditions.append(f'cf[13303] = "{qa_required}"')
    if dependent_systems:
        jql_conditions.append(f'cf[15506] = "{dependent_systems}"')
    if epic_link:
        jql_conditions.append(f'cf[10008] = "{epic_link}"')
    if sprint:
        jql_conditions.append(f'cf[10007] = "{sprint}"')
    if priority:
        jql_conditions.append(f'priority = "{priority}"')
    if issue_type:
        jql_conditions.append(f'issuetype = "{issue_type}"')
    if status:
        joined = ', '.join(f'"{s}"' for s in status)
        jql_conditions.append(f"status in ({joined})")

    jql = " AND ".join(jql_conditions) + " ORDER BY updated DESC"
    return await search_issues(jql, max_results)

@mcp.tool()
async def update_jira_ticket_tool(
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
    Update an existing Jira ticket with specified parameters.

    Args:
        issue_key (str): The key of the Jira ticket to update (e.g., 'FCA-1234').
        summary (str): Updated title/summary of the Jira ticket.
        description (str): Updated description of the issue.
        status_name (str): The **name** of the status to transition the ticket to (e.g., "In Progress", "Closed")
        priority (str): Updated priority level of the ticket.
        assignee (str): Username of the person to whom the ticket should be reassigned.
        fin_business_cost_center (List[str]): Updated financial business cost center for the ticket.
        flows (str): Updated workflow flows associated with the ticket.
        tag_types (str): Updated types of tags to be associated with the ticket.
        beat_types (str): Updated types of beats related to the ticket.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - isIssueUpdated (bool): Whether the update was successful
            - response (str): Success message if update was successful
            - error (str): Error message if update failed
    """
    from utils.issue.update import update_jira_ticket
    return await update_jira_ticket(
        issue_key=issue_key,
        summary=summary,
        description=description,
        status_name=status_name,
        priority=priority,
        assignee=assignee,
        fin_business_cost_center=fin_business_cost_center,
        flows=flows,
        tag_types=tag_types,
        beat_types=beat_types,
    )

# Create SSE transport for /jira/messages/
sse = SseServerTransport("/jira/messages/")

# Route for posting messages
messages_route = Mount("/jira/messages/", app=sse.handle_post_message)

# Route for SSE stream
async def handle_sse(request):
    # Create initialization options with proper session setup
    init_options = mcp._mcp_server.create_initialization_options()
    
    # Ensure we wait for proper initialization
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        try:
            # Run the server with initialization options
            await mcp._mcp_server.run(
                streams[0],
                streams[1],
                init_options,
            )
        except Exception as e:
            print(f"Error in MCP server: {str(e)}")
            raise

sse_route = Route("/jira/sse", endpoint=handle_sse)

# Create Starlette app
app = Starlette(
    debug=True,
    routes=[messages_route, sse_route]
)

if __name__ == "__main__":
    
    config = uvicorn.Config(
        app,
        host=SERVER_HOST,
        port=SERVER_PORT,
        log_level="info",
    )
    server = uvicorn.Server(config)
    import asyncio
    asyncio.run(server.serve())
