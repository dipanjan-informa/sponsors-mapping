from aws_cdk import Duration, Stack
from constructs import Construct
from resources import ResourceRegistry
from environment import ENVIRONMENT_CONFIG
from aws_cdk import aws_lambda as _lambda
from aws_cdk.aws_lambda import Runtime


class MainStack(Stack):

    def __init__(self, scope: Construct, id, **kwargs):
        super().__init__(scope, id, **kwargs)
        self.config = ENVIRONMENT_CONFIG
        self.resource_registry = ResourceRegistry()

        # Create the Lambda function
        self.sponsors_lambda = self._create_sponsors_lambda()

        # Register the Lambda in the resource registry
        self.resource_registry.sponsors_lambda = self.sponsors_lambda

    def _create_sponsors_lambda(self) -> _lambda.Function:
        return _lambda.Function(
            self,
            f"{self.config.resource_prefix}-Sponsors",
            function_name=f"{self.config.resource_prefix}-Sponsors",
            runtime=Runtime.PYTHON_3_13,
            handler="handler.handler",
            code=_lambda.Code.from_asset("src/sponsors"),
            layers=[],
            environment={
                "DB_HOST": self.config.db_host or "localhost",
                "DB_PORT": str(self.config.db_port or 5432),
                "DB_NAME": self.config.db_name or "sponsors_db",
                "DB_USER": self.config.db_user or "admin",
                "DB_PASSWORD": self.config.db_password or "password",
            },
            timeout=Duration.seconds(30),
        )
