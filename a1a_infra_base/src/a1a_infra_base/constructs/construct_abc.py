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
from typing import Any, Self

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
