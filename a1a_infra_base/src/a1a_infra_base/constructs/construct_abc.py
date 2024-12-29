"""
Module construct_abc

This module defines abstract base classes for configuration and level 0 constructs.

Classes:
    ConstructABC: Abstract base class for configuration classes.
    ConstructL0ABC: Abstract base class for level 0 constructs.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Final, Self

from a1a_infra_base.logger import setup_logger

logger: logging.Logger = setup_logger(__name__)

# Constants for dictionary keys
NAME_KEY: Final[str] = "name"


class ConstructABC(ABC):
    """
    Abstract base class for configuration classes.

    Methods:
        from_config: Create a configuration instance by unpacking parameters from a configuration dictionary.
    """

    @classmethod
    @abstractmethod
    def from_config(cls, env: str, config: dict[str, Any]) -> Self:
        """
        Create a configuration instance by unpacking parameters from a configuration dictionary.

        Args:
            env (str): The environment name.
            config (dict): A dictionary containing management lock configuration.

        Returns:
            ConstructABC: A fully-initialized configuration instance.
        """


class ConstructL0ABC(ConstructABC, ABC):
    """
    Abstract base class for level 0 constructs.

    Properties:
        full_name: Generates the full name for the configuration.
    """

    @property
    @abstractmethod
    def full_name(self) -> str:
        """Generates the full name for the configuration."""
