import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()


@dataclass
class Environment:
    """Configuration for Environment Variables"""

    # AWS Settings
    aws_account_id: str = None
    aws_region: str = None

    # Application Settings
    app_name: str = None
    environment: str = None

    # Database Settings
    db_host: str = None
    db_port: int = None
    db_name: str = None
    db_user: str = None
    db_password: str = None

    # Initialize Environment
    def __init__(self):
        # AWS Settings
        self.aws_account_id = os.getenv("AWS_ACCOUNT_ID")
        self.aws_region = os.getenv("AWS_REGION")

        # Application Settings
        self.app_name = os.getenv("APP_NAME")
        self.environment = os.getenv("ENVIRONMENT")

        # Database Settings
        self.db_host = os.getenv("DB_HOST")
        self.db_port = int(os.getenv("DB_PORT", "5432"))
        self.db_name = os.getenv("DB_NAME")
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")

    # Resource Prefix
    @property
    def resource_prefix(self) -> str:
        return f"{self.app_name}-{self.environment}"


ENVIRONMENT_CONFIG = Environment()
