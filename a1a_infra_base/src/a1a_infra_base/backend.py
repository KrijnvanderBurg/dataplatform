"""
Module backend

This module defines the BackendConfig class, which is responsible for representing
the backend configuration for Terraform stacks.

Classes:
    BackendConfig: A class to represent the backend configuration.
"""

from dataclasses import dataclass
from typing import Any, Final

# Constants for dictionary keys
PATH_KEY: Final[str] = "path"


@dataclass
class BackendConfig:
    """
    A class to represent the backend configuration.

    Attributes:
        path (str): The path for the local backend.
    """

    path: str

    @classmethod
    def from_dict(cls, config: dict[str, Any]) -> "BackendConfig":
        """
        Create a BackendConfig instance from a configuration dictionary.

        Args:
            config (dict): A dictionary containing backend configuration.

        Returns:
            BackendConfig: A fully-initialized BackendConfig instance.
        """
        path = config[PATH_KEY]
        return cls(path=path)
