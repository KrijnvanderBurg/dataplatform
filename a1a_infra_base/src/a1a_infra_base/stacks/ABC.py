"""
Module ABC

This module defines abstract base classes for stack configurations.

Classes:
    ConstructABC: Abstract base class for configuration classes.
    ConstructL0ABC: Abstract base class for level 0 constructs.
"""

import logging
from abc import ABC, ABCMeta, abstractmethod
from typing import Any, Final, Self

from jsii import JSIIMeta

from a1a_infra_base.logger import setup_logger
from constructs import Construct

logger: logging.Logger = setup_logger(__name__)


# Constants for dictionary keys
BACKEND_KEY: Final[str] = "terraform_backend"
LOCAL_KEY: Final[str] = "local"

PROVIDER_KEY: Final[str] = "terraform_provider"
AZURERM_KEY: Final[str] = "azurerm"

CONSTRUCTS_KEY: Final[str] = "constructs"


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


class CombinedMeta(JSIIMeta, ABCMeta):
    """
    Meta class combining CDKTF.Construct and ABCMeta.

    This class is used to combine the Stack super class with the a1a_infra_base.StackABC.
    """


class StackABC(ABC):
    """
    Abstract base class for stacks.
    """

    @abstractmethod
    def __init__(self, scope: Construct, id_: str, *, env: str, config: StackConfigABC) -> None:
        """
        Initializes the StackABC construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            config (StackConfigABC): The configuration for the stack.
        """
