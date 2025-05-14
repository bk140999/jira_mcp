# MCP Jira

Model Context Protocol (MCP) server for Jira. This integration supports updating Jira dashboards.

## Example Usage

Ask your AI assistant to:

- **📝 Create Jira Tickets** - Create Jira tickets right from cursor
- **📄 Get project info** - Fetch project info using key or peject id
- **📄 Get project search option** - search project on various inputs
- **✏️ Get Jira Comment** - Get Jira comment by providing the issue key
- **💬 Add Jira Comment** - Add a new comment to a Jira issue using the issue key and comment content
- **🛠️ Update Jira Fields** - Modify fields like summary, status, or priority on a Jira issue using the issue key and field values







## Quick Start Guide

### 1. Authentication Setup

First, generate the necessary authentication tokens for Jira:

#### For Cloud

1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click **Create API token**, name it
3. Copy the token 
#### For Self Hosted

1. Go to your profile
2. Click **Create Personal Access token**, name it
3. Copy the token 

After generating token create an .env file and add following keys
JIRA_BASE_URL=""
JIRA_USER_EMAIL=""
JIRA_API_TOKEN=""
JIRA_USER_ID=""
JIRA_SESSION_COOKIE=""

### 2. Installation

1. Clone this repo.
2. Run `pip install requirements.txt`.
3. Run `python jira.py`

#### IDE Integration

MCP Jira can work with your favorite IDE.

Example: Cursor Configuration

```json
{
  "mcpServers": {
    "jira": {
      "url": "http://127.0.0.1:7777/jira/sse"
    }
  }
}

```

## Remarks 
You are ready to use all the tools available in this mcp server


