"""AWS service package for the eraXplor FOCUS workflow.

This package exposes the AWS CLI entry point implemented in
`core.services.aws.__main__` and the supporting utility modules under
`core.services.aws.utils`.
"""

from .__main__ import main

__all__ = ["main"]