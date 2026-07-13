"""Azure service package for the eraXplor FOCUS workflow.

This package exposes the Azure CLI entry point implemented in
`core.services.azure.__main__` and the supporting utility modules under
`core.services.azure.utils`.
"""

from .__main__ import main

__all__ = ["main"]