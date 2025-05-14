import os
from typing import Optional

class JiraConfig:
    BASE_URL: str = os.getenv('JIRA_BASE_URL')
    USER_EMAIL: str = os.getenv('JIRA_USER_EMAIL')
    API_TOKEN: str = os.getenv('JIRA_API_TOKEN')
    USER_ID: str = os.getenv('JIRA_USER_ID')
    SESSION_COOKIE: Optional[str] = os.getenv('JIRA_SESSION_COOKIE')

    @classmethod
    def validate_config(cls) -> None:
        required_vars = {
            'JIRA_BASE_URL': cls.BASE_URL,
            'JIRA_USER_EMAIL': cls.USER_EMAIL,
            'JIRA_API_TOKEN': cls.API_TOKEN,
            'JIRA_USER_ID': cls.USER_ID,
        }
        
        missing_vars = [var for var, value in required_vars.items() if not value]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}") 