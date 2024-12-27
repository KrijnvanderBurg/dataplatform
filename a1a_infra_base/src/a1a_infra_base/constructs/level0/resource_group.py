"""
Module resource_group

This module defines the ResourceGroupL0 class, which is responsible for creating
and managing an Azure resource group with specific configurations.

Classes:
    ResourceGroupL0: A level 0 construct that creates and manages an Azure resource group.
"""

from typing import Final

from cdktf_cdktf_provider_azurerm.resource_group import ResourceGroup
from constructs import Construct

from a1a_infra_base.constants import AzureLocation, AzureResource

# Constants for dictionary keys
NAME_KEY: Final[str] = "name"
LOCATION_KEY: Final[str] = "location"
SEQUENCE_NUMBER_KEY: Final[str] = "sequence_number"


class ResourceGroupL0(Construct):
    """
    A level 0 construct that creates and manages an Azure resource group.

    Attributes:
        resource_group (ResourceGroup): The Azure resource group.
    """

    def __init__(
        self, scope: Construct, id_: str, *, env: str, name: str, location: AzureLocation, sequence_number: str
    ) -> None:
        """
        Initializes the ResourceGroupL0 construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            name (str): The name of the resource group.
            location (AzureLocation): The Azure location.
            sequence_number (str): The sequence number.
        """
        super().__init__(scope, id_)
        self._resource_group = ResourceGroup(
            self,
            f"{AzureResource.RESOURCE_GROUP.abbr}_{name}_{env}_{location.abbr}_{sequence_number}",
            name=f"{AzureResource.RESOURCE_GROUP.abbr}-{name}-{env}-{location.abbr}-{sequence_number}",
            location=location.name,
        )

    @property
    def resource_group(self) -> ResourceGroup:
        """Gets the Azure resource group."""
        return self._resource_group

    @classmethod
    def from_config(cls, scope: Construct, id_: str, env: str, config: dict) -> "ResourceGroupL0":
        """
        Create a ResourceGroupL0 construct by unpacking parameters from a configuration dictionary.

        Expected format of 'config':
        {
            "name": "<resource group name>",
            "location": "<AzureLocation enum value name>",
            "sequence_number": "<sequence number>"
        }

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            config (dict): A dictionary containing resource group configuration.

        Returns:
            ResourceGroupL0: A fully-initialized ResourceGroupL0 construct.
        """
        name = config[NAME_KEY]
        location = AzureLocation(config[LOCATION_KEY])
        sequence_number = config[SEQUENCE_NUMBER_KEY]

        return cls(scope, id_, name=name, env=env, location=location, sequence_number=sequence_number)
