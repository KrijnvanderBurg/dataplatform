"""
Module construct_abc

This module defines abstract base classes for configuration and level 0 constructs.

Classes:
    ConstructABC: Abstract base class for configuration classes.
    ConstructL0ABC: Abstract base class for level 0 constructs.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Self

from constructs import Construct

from a1a_infra_base.logger import setup_logger

logger: logging.Logger = setup_logger(__name__)


class ConstructConfigABC(ABC):
    """
    Abstract base class for configuration classes.

    Methods:
        from_config: Create a configuration instance by unpacking parameters from a configuration dictionary.
    """

    @classmethod
    @abstractmethod
    def from_dict(cls, config: dict[str, Any]) -> Self:
        """
        Create a configuration instance by unpacking parameters from a configuration dictionary.

        Args:
            config (dict): A dictionary containing management lock configuration.

        Returns:
            ConstructABC: A fully-initialized configuration instance.
        """


class ConstructABC(ABC):
    """
    Abstract base class for level 0 constructs.

    Properties:
        full_name: Generates the full name for the configuration.
    """

    @property
    @abstractmethod
    def full_name(self) -> str:
        """Generates the full name for the configuration."""

    @classmethod
    @abstractmethod
    def from_config(cls, scope: Construct, id_: str, env: str, config: dict) -> Self:
        """
        Abstract method to create a construct from a configuration dictionary.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            config (dict): The configuration dictionary.

        Returns:
            Self: A fully-initialized construct instance.
        """
