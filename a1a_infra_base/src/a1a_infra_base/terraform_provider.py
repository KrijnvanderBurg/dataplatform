"""
Module provider

This module defines the ProviderConfig class for Terraform providers.

Classes:
    ProviderConfig: A class to represent the provider configuration.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Final, Self

# Constants for dictionary keys
TENANT_ID: Final[str] = "tenant_id"
SUBSCRIPTION_ID: Final[str] = "subscription_id"
CLIENT_ID: Final[str] = "client_id"
CLIENT_SECRET: Final[str] = "client_secret"


@dataclass
class TerraformProviderConfigABC(ABC):
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
class TerraformProviderAzurermConfig(TerraformProviderConfigABC):
    """
    A class to represent the Azurerm provider configuration.

    Attributes:
        path (str): The path for the local provider.
    """

    tenant_id: str
    subscription_id: str
    client_id: str
    client_secret: str

    @classmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Create a AzurermProviderConfig instance from a configuration dictionary.

        Args:
            dict_ (dict): A dictionary containing provider configurations.

        Returns:
            AzurermProviderConfig: A fully-initialized AzurermProviderConfig instance.
        """
        tenant_id: str = dict_[TENANT_ID]
        subscription_id: str = dict_[SUBSCRIPTION_ID]
        client_id: str = dict_[CLIENT_ID]
        client_secret: str = dict_[CLIENT_SECRET]
        return cls(
            tenant_id=tenant_id, subscription_id=subscription_id, client_id=client_id, client_secret=client_secret
        )
