"""
Module construct_abc

This module defines abstract base classes for configuration and level 0 constructs.

Classes:
    ConstructABC: Abstract base class for configuration classes.
    ConstructL0ABC: Abstract base class for level 0 constructs.
"""

import logging
from abc import ABC, ABCMeta, abstractmethod
from typing import Any, Generic, Self, TypeVar

from constructs import Construct
from jsii import JSIIMeta

from a1a_infra_base.logger import setup_logger

logger: logging.Logger = setup_logger(__name__)


class CombinedMeta(JSIIMeta, ABCMeta):
    """TODO"""


class ConstructConfigABC(ABC):
    """
    Abstract base class for configuration classes.

    Methods:
        from_config: Create a configuration instance by unpacking parameters from a configuration dictionary.
    """

    @classmethod
    @abstractmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Create a configuration instance by unpacking parameters from a configuration dictionary.

        Args:
            dict_ (dict): A dictionary containing management lock configuration.

        Returns:
            ConstructABC: A fully-initialized configuration instance.
        """


class ConstructABC(ABC):
    """
    Abstract base class for level 0 constructs.

    Properties:
        full_name: Generates the full name for the configuration.
    """

    def __init__(self) -> None:
        self._full_name: str = ""

    @property
    def full_name(self) -> str:
        """Generates the full name for the configuration.

        Returns:
            str: The full name for the construct.
        """
        return self._full_name

    @full_name.setter
    def full_name(self, value: str) -> None:
        """
        Sets the full name for the resource group.

        Args:
            value (str): The full name to set.
        """
        self._full_name = value


T = TypeVar("T", bound=ConstructConfigABC)


class DetachedConstructABC(ConstructABC, Generic[T]):
    """
    Abstract base class for level 0 constructs without dynamically attached resources.

    Properties:
        full_name: Generates the full name for the configuration.
    """

    @classmethod
    @abstractmethod
    def from_config(cls, scope: Construct, id_: str, env: str, config: T) -> Self:
        """
        Abstract method to create a construct from a configuration dictionary.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            config (T): The configuration object.

        Returns:
            Self: A fully-initialized construct instance.
        """


class AttachedConstructABC(ConstructABC, Generic[T]):
    """
    Abstract base class for level 0 constructs with dynamically attached resources.

    Properties:
        full_name: Generates the full name for the configuration.
    """

    @classmethod
    @abstractmethod
    def from_config(cls, scope: Construct, id_: str, env: str, attach_to_resource_id: str, config: T) -> Self:
        """
        Abstract method to create a construct from a configuration dictionary.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            attach_to_resource_id (str): The resource ID to attach to.
            config (T): The configuration object.

        Returns:
            Self: A fully-initialized construct instance.
        """
