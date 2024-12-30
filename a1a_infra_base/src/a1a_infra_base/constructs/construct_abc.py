"""
Module construct_abc

This module defines abstract base classes for construct configurations and constructs.

Classes:
    CombinedMeta: Meta class combining JSIIMeta and ABCMeta.
    ConstructConfigABC: Abstract base class for construct configuration classes.
    ConstructABC: Abstract base class for constructs.
    DetachedConstructABC: Abstract base class for constructs without dynamically attached resources.
    AttachedConstructABC: Abstract base class for constructs with dynamically attached resources.
"""

import logging
from abc import ABC, ABCMeta, abstractmethod
from typing import Any, Generic, Self, TypeVar

from constructs import Construct
from jsii import JSIIMeta

from a1a_infra_base.logger import setup_logger

logger: logging.Logger = setup_logger(__name__)


class ConstructConfigABC(ABC):
    """
    Abstract base class for construct configuration classes.

    Methods:
        from_dict: Create a configuration instance by unpacking parameters from a construct configuration dictionary.
    """

    @classmethod
    @abstractmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Create a construct configuration instance by unpacking parameters from a construct configuration dictionary.

        Args:
            dict_ (dict): A dictionary containing management lock configuration.

        Returns:
            ConstructABC: A fully-initialized configuration instance.
        """


class CombinedMeta(JSIIMeta, ABCMeta):
    """
    Meta class combining CDKTF.Construct and ABCMeta.

    This class is used to combine the Construct super class with the a1a_infra_base.ConstructABC.
    """


class ConstructABC(ABC):
    """
    Abstract base class for constructs.

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
    Abstract base class for constructs without dynamically attached resources.

    Methods:
        from_config: Create a construct from a configuration dictionary.
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
    Abstract base class for constructs with dynamically attached resources.

    Methods:
        from_config: Create a construct from a configuration dictionary.
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
