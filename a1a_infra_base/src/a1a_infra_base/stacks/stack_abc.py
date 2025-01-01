"""
Module construct_abc

This module defines abstract base classes for stack configurations.

Classes:
    ConstructABC: Abstract base class for configuration classes.
    ConstructL0ABC: Abstract base class for level 0 constructs.
"""

import logging
from abc import ABC, ABCMeta, abstractmethod
from typing import Any, Self

from constructs import Construct
from jsii import JSIIMeta

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


class CombinedMeta(JSIIMeta, ABCMeta):
    """
    Meta class combining CDKTF.Construct and ABCMeta.

    This class is used to combine the Stack super class with the a1a_infra_base.StackABC.
    """


class StackABC(ABC):
    """
    Abstract base class for stacks.
    """

    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        env: str,
        config: StackConfigABC,
    ) -> None:
        """
        Initialize a new stack.

        Args:
            scope (Construct): The parent construct.
            id_ (str): The ID of the stack.
            env (str): The environment.
            config (StackConfigABC): The stack configuration.
        """
