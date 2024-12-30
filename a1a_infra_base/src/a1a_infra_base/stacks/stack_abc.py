"""
Module construct_abc

This module defines abstract base classes for stack configurations.

Classes:
    ConstructABC: Abstract base class for configuration classes.
    ConstructL0ABC: Abstract base class for level 0 constructs.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Self

from a1a_infra_base.logger import setup_logger

logger: logging.Logger = setup_logger(__name__)


class StackConfigABC(ABC):
    """
    Abstract base class for stack configuration classes.

    Methods:
        from_config: Create a configuration instance by unpacking parameters from a stack configuration dictionary.
    """

    @classmethod
    @abstractmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Create a stack configuration instance by unpacking parameters from a stack configuration dictionary.

        Args:
            dict_ (dict): A dictionary containing management lock configuration.

        Returns:
            ConstructABC: A fully-initialized configuration instance.
        """
