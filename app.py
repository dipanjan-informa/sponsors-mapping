#!/usr/bin/env python3
import aws_cdk as cdk
from environment import ENVIRONMENT_CONFIG
from main_stack import MainStack


app = cdk.App()
MainStack(
    app,
    f"{ENVIRONMENT_CONFIG.resource_prefix}-Stack",
    env=cdk.Environment(
        account=ENVIRONMENT_CONFIG.aws_account_id,
        region=ENVIRONMENT_CONFIG.aws_region,
    ),
)

app.synth()
