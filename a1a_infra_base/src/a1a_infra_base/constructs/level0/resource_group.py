"""
Module resource_group

This module defines the ResourceGroupL0 class and the ResourceGroupConfig class,
which are responsible for creating and managing an Azure resource group with specific configurations.

Classes:
    ResourceGroupL0: A level 0 construct that creates and manages an Azure resource group.
    ResourceGroupConfig: A configuration class for ResourceGroupL0.
"""

from dataclasses import dataclass
from typing import Any, Final, Self

from cdktf_cdktf_provider_azurerm.resource_group import ResourceGroup
from constructs import Construct

from a1a_infra_base.constants import AzureLocation, AzureResource

# Constants for dictionary keys
NAME_KEY: Final[str] = "name"
LOCATION_KEY: Final[str] = "location"
SEQUENCE_NUMBER_KEY: Final[str] = "sequence_number"
ENV_KEY: Final[str] = "env"


@dataclass
class ResourceGroupL0Config:
    """
    A configuration class for ResourceGroupL0.

    Attributes:
        env (str): The environment name.
        name (str): The name of the resource group.
        location (AzureLocation): The Azure location.
        sequence_number (str): The sequence number.
    """

    env: str
    name: str
    location: AzureLocation
    sequence_number: str

    @property
    def full_name(self) -> str:
        """Generates the full name for the resource group."""
        return f"{AzureResource.RESOURCE_GROUP.abbr}-{self.name}-{self.env}-{self.location.abbr}-{self.sequence_number}"

    @classmethod
    def from_config(cls, env: str, config: dict[str, Any]) -> Self:
        """
        Create a ResourceGroupConfig by unpacking parameters from a configuration dictionary.

        Expected format of 'config':
        {
            "name": "<resource group name>",
            "location": "<AzureLocation enum value name>",
            "sequence_number": "<sequence number>"
        }

        Args:
            env (str): The environment name.
            config (dict): A dictionary containing resource group configuration.

        Returns:
            ResourceGroupConfig: A fully-initialized ResourceGroupConfig.
        """
        name = config[NAME_KEY]
        location = AzureLocation.from_full_name(config[LOCATION_KEY])
        sequence_number = config[SEQUENCE_NUMBER_KEY]

        return cls(env=env, name=name, location=location, sequence_number=sequence_number)


class ResourceGroupL0(Construct):
    """
    A level 0 construct that creates and manages an Azure resource group.

    Attributes:
        resource_group (ResourceGroup): The Azure resource group.
    """

    def __init__(self, scope: Construct, id_: str, *, config: ResourceGroupL0Config) -> None:
        """
        Initializes the ResourceGroupL0 construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            config (ResourceGroupConfig): The configuration for the resource group.
        """
        super().__init__(scope, id_)
        self._resource_group = ResourceGroup(
            self,
            f"ResourceGroup_{config.full_name}",
            name=config.full_name,
            location=config.location.full_name,
        )

    @property
    def resource_group(self) -> ResourceGroup:
        """Gets the Azure resource group."""
        return self._resource_group
