from dataclasses import dataclass
from typing import Optional, Dict
from aws_cdk import (
    aws_lambda as _lambda,
)


@dataclass
class ResourceRegistry:
    """Centralized Registry for tracking resource ARNs and other shared values"""

    sponsors_lambda: Optional[_lambda.Function] = None

    # Custom Method to get all ARNs as dict
    def to_dict(self) -> Dict[str, str]:
        return {k: v for k, v in self.__dict__.items() if v is not None}
