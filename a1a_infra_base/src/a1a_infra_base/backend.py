"""
Module backend

This module defines the BackendConfig class, which is responsible for representing
the backend configuration for Terraform stacks.

Classes:
    BackendConfig: A class to represent the backend configuration.
"""

from typing import Any, Final, Self

# Constants for dictionary keys
PATH_KEY: Final[str] = "path"


class BackendConfig:
    """
    A class to represent the backend configuration.

    Attributes:
        path (str): The path for the local backend.
    """

    def __init__(self, path: str) -> None:
        """
        Initializes the BackendConfig.

        Args:
            path (str): The path for the local backend.
        """
        self.path = path

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> Self:
        """
        Create a BackendConfig instance from a configuration dictionary.

        Args:
            config (dict): A dictionary containing backend configuration.

        Returns:
            BackendConfig: A fully-initialized BackendConfig instance.
        """
        path = config[PATH_KEY]
        return cls(path=path)
