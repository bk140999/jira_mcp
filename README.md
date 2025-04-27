# MCP Jira

Model Context Protocol (MCP) server for Jira. This integration supports updating Jira dashboards.

## Example Usage

Ask your AI assistant to:

- **📝 Create Jira Tickets** - Create Jira tickets right from cursor
- **📄 Get project info** - Fetch project info

### Feature Demo

![Demo](https://github.com/TusharShahi/mcp-jira/blob/master/demo/recording.gif)


## Quick Start Guide

### 1. Authentication Setup

First, generate the necessary authentication tokens for Jira:

#### For Cloud

1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click **Create API token**, name it
3. Copy the token 

### 2. Installation

1. Clone this repo.
2. Install `uv`.

#### IDE Integration

MCP Jira can work with your favorite IDE.

Example: Cursor Configuration

```json
{
  "mcpServers": {
    "jira": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/PATH/TO/jira/server",
        "run",
        "jira.py"
      ],
      "env": {
        "JIRA_API_TOKEN": "XXXX",
        "JIRA_BASE_URL": "XXXX",
        "JIRA_USER_EMAIL": "XXXX",
        "JIRA_USER_ID": "XXXX" 
      }
    },
  }
}

```

## Remarks 

This is not an official Atlassian product.

