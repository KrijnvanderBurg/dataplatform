"""
Module provider

This module defines the ProviderConfig class for Terraform providers.

Classes:
    ProviderConfig: A class to represent the provider configuration.
"""

from abc import ABC, ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Any, Final, Self

from cdktf import TerraformStack
from cdktf_cdktf_provider_azurerm.provider import AzurermProvider
from constructs import Construct
from jsii import JSIIMeta

# Constants for dictionary keys
NAME_KEY: Final[str] = "name"

PROVIDER_AZURERM: Final[str] = "azurerm"


class CombinedMeta(JSIIMeta, ABCMeta):
    """
    Meta class combining CDKTF.Construct and ABCMeta.

    This class is used to combine the Construct super class with the a1a_infra_base.ConstructABC.
    """


@dataclass
class ProviderConfigABC(ABC):
    """
    Abstract base class for provider configuration classes.

    Methods:
        from_dict: Create a configuration instance by unpacking parameters from a provider configuration dictionary.
    """

    @classmethod
    @abstractmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Create a provider configuration instance by unpacking parameters from a provider configuration dictionary.

        Args:
            dict_ (dict): A dictionary containing provider configuration.

        Returns:
            ProviderConfigABC: A fully-initialized provider configuration instance.
        """


@dataclass
class ProviderAzurermConfig(TerraformStack, ProviderConfigABC, metaclass=CombinedMeta):
    """
    A class to represent the Azurerm provider configuration.

    Attributes:
        path (str): The path for the local provider.
    """

    name: str

    @classmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Create a AzurermProviderConfig instance from a configuration dictionary.

        Args:
            dict_ (dict): A dictionary containing provider configurations.

        Returns:
            AzurermProviderConfig: A fully-initialized AzurermProviderConfig instance.
        """
        name = dict_[NAME_KEY]
        return cls(name=name)


class ProviderAzurerm:
    """TODO"""

    def __init__(self, scope: Construct, *, name: str) -> None:
        AzurermProvider(scope, name, features=[{}])

    @classmethod
    def from_config(cls, scope: Construct, *, config: ProviderAzurermConfig) -> Self:
        """TODO"""
        return cls(scope, name=config.name)


MAPPING_PROVIDERS: Final[dict[str, Any]] = {PROVIDER_AZURERM: (ProviderAzurermConfig, ProviderAzurerm),}


@dataclass
class ProviderConfigFactory:
    """TODO
    """

    @staticmethod
    def from_dicts(dict_: dict[str, Any]) -> list[ProviderConfigABC]:
        """
        Create a ProviderConfig instance from a configuration dictionary.

        Args:
            dict_ (dict[str, Any]): A dictionary containing provider configurations.

        Returns:
            list[ProviderConfigABC]: A list of ProviderConfig instances.
        """
        providers: list[ProviderConfigABC] = []

        for key in dict_.keys():
            if key not in MAPPING_PROVIDERS:
                raise ValueError(f"Unknown provider name: {key}")

            provider_config_cls, _ = MAPPING_PROVIDERS[key]
            providers.append(provider_config_cls.from_dict(dict_=dict_[key]))
        return providers


@dataclass
class ProviderFactory:
    """TODO
    """

    @staticmethod
    def from_configs(scope: Construct, configs: list[ProviderConfigABC]) -> None:
        """
        Create a ProviderConfig instance from a configuration dictionary.

        Args:
            configs (list[ProviderConfigABC]): A list of provider configs.
        """


        if configs. not in MAPPING_PROVIDERS:
            raise ValueError(f"Unknown provider name: {key}")

        provider_cls, _ = MAPPING_PROVIDERS[key]
        provider_cls.from_config(scope, config=configs)
