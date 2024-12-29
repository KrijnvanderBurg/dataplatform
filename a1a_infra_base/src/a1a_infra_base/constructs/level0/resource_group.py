"""
Module resource_group

This module defines the ResourceGroupL0 class and the ResourceGroupConfig class,
which are responsible for creating and managing an Azure resource group with specific configurations.

Classes:
    ResourceGroupL0: A level 0 construct that creates and manages an Azure resource group.
    ResourceGroupConfig: A configuration class for ResourceGroupL0.
"""

import logging
from dataclasses import dataclass
from typing import Any, Final, Self

from cdktf_cdktf_provider_azurerm.resource_group import ResourceGroup
from constructs import Construct

from a1a_infra_base.constants import AzureLocation, AzureResource
from a1a_infra_base.constructs.construct_abc import ConstructL0ABC
from a1a_infra_base.constructs.level0.management_lock import ManagementLockL0, ManagementLockL0Config
from a1a_infra_base.logger import setup_logger

logger: logging.Logger = setup_logger(__name__)

# Constants for dictionary keys
NAME_KEY: Final[str] = "name"
LOCATION_KEY: Final[str] = "location"
SEQUENCE_NUMBER_KEY: Final[str] = "sequence_number"
ENV_KEY: Final[str] = "env"
MANAGEMENT_LOCK_KEY: Final[str] = "management_lock"


@dataclass
class ResourceGroupL0Config(ConstructL0ABC):
    """
    A configuration class for ResourceGroupL0.

    Attributes:
        env (str): The environment name.
        name (str): The name of the resource group.
        location (AzureLocation): The Azure location.
        sequence_number (str): The sequence number.
        management_lock (ManagementLockL0Config | None): The management lock configuration.
    """

    env: str
    name: str
    location: AzureLocation
    sequence_number: str
    management_lock: ManagementLockL0Config | None = None

    @property
    def full_name(self) -> str:
        """
        Generates the full name for the resource group.

        Returns:
            str: The full name of the resource group.
        """
        return f"{AzureResource.RESOURCE_GROUP.abbr}-{self.name}-{self.env}-{self.location.abbr}-{self.sequence_number}"

    @classmethod
    def from_config(cls, env: str, config: dict[str, Any]) -> Self:
        """
        Create a ResourceGroupConfig by unpacking parameters from a configuration dictionary.

        Expected format of 'config':
        {
            "name": "<resource group name>",
            "location": "<AzureLocation enum value name>",
            "sequence_number": "<sequence number>",
            "management_lock": {
                "lock_level": "<lock level>",
                "notes": "<notes>"
            }
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

        management_lock = config.get(MANAGEMENT_LOCK_KEY, None)
        if management_lock:
            management_lock = ManagementLockL0Config.from_config(env=env, config=config[MANAGEMENT_LOCK_KEY])

        return cls(
            env=env,
            name=name,
            location=location,
            sequence_number=sequence_number,
            management_lock=management_lock,
        )


class ResourceGroupL0(Construct):
    """
    A level 0 construct that creates and manages an Azure resource group.

    Attributes:
        resource_group (ResourceGroup): The Azure resource group.
        management_lock (ManagementLockL0 | None): The management lock applied to the resource group.
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

        if config.management_lock:
            self._management_lock: ManagementLockL0 | None = ManagementLockL0(
                self,
                "ManagementLockL0",
                name=config.full_name,
                config=config.management_lock,
                resource_id=self.resource_group.id,
            )
        else:
            self._management_lock = None

    @property
    def resource_group(self) -> ResourceGroup:
        """Gets the Azure resource group."""
        return self._resource_group

    @property
    def management_lock(self) -> ManagementLockL0 | None:
        """Gets the management lock applied to the resource group."""
        return self._management_lock
