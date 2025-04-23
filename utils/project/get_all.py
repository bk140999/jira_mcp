import httpx
import json

from utils.config import JiraConfig

async def get_all_projects():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{JiraConfig.BASE_URL}/rest/api/3/project/search",
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                auth=(JiraConfig.USER_EMAIL, JiraConfig.API_TOKEN)
            )
            response.raise_for_status()
            data = response.json()
            projects = data.get('values', [])
            print("projects")
            print(projects)
            return projects
    except httpx.RequestError as e:
        print(f"Error fetching projects: {e}")
        raise
