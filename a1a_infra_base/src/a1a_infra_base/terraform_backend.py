"""
Module backend

This module defines the BackendConfig class, which is responsible for representing
the backend configuration for Terraform stacks.

Classes:
    BackendConfig: A class to represent the backend configuration.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Final, Self

# Constants for dictionary keys
PATH_KEY: Final[str] = "path"


@dataclass
class TerraformBackendConfigABC(ABC):
    """
    Abstract base class for backend configuration classes.

    Methods:
        from_dict: Create a configuration instance by unpacking parameters from a backend configuration dictionary.
    """

    @classmethod
    @abstractmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Create a backend configuration instance by unpacking parameters from a backend configuration dictionary.

        Args:
            dict_ (dict): A dictionary containing backend configuration.

        Returns:
            backendConfigABC: A fully-initialized backend configuration instance.
        """


@dataclass
class TerraformBackendLocalConfig(TerraformBackendConfigABC):
    """
    A class to represent the local backend configuration.

    Attributes:
        path (str): The path for the local backend.
    """

    path: str

    @classmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Create a BackendConfig instance from a configuration dictionary.

        Args:
            dict_ (dict): A dictionary containing backend configuration.

        Returns:
            BackendConfig: A fully-initialized BackendConfig instance.
        """
        path = dict_[PATH_KEY]
        return cls(path=path)
