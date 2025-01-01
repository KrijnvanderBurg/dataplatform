"""
Module resource_group

This module defines the ResourceGroupL0 class and the ResourceGroupL0Config class,
which are responsible for creating and managing an Azure resource group with specific configurations.

Classes:
    ResourceGroupL0: A level 0 construct that creates and manages an Azure resource group.
    ResourceGroupL0Config: A configuration class for ResourceGroupL0.
"""

import logging
from dataclasses import dataclass
from typing import Any, Final, Self

from cdktf_cdktf_provider_azurerm.resource_group import ResourceGroup
from constructs import Construct

from a1a_infra_base.constants import AzureLocation, AzureResource
from a1a_infra_base.constructs.construct_abc import CombinedMeta, ConstructABC, ConstructConfigABC
from a1a_infra_base.constructs.level0.management_lock import ManagementLockL0, ManagementLockL0Config
from a1a_infra_base.logger import setup_logger

logger: logging.Logger = setup_logger(__name__)

# Constants for dictionary keys
NAME_KEY: Final[str] = "name"
LOCATION_KEY: Final[str] = "location"
SEQUENCE_NUMBER_KEY: Final[str] = "sequence_number"
MANAGEMENT_LOCK_KEY: Final[str] = "management_lock"


@dataclass
class ResourceGroupL0Config(ConstructConfigABC):
    """
    A configuration class for ResourceGroupL0.

    Attributes:
        name (str): The name of the resource group.
        location (AzureLocation): The Azure location.
        sequence_number (str): The sequence number.
        management_lock (ManagementLockL0Config | None): The management lock configuration.
    """

    name: str
    location: AzureLocation
    sequence_number: str
    management_lock: ManagementLockL0Config | None = None

    @classmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Create a ResourceGroupL0Config instance by unpacking parameters from a configuration dictionary.

        The expected format of 'dict_' is:
        {
            "name": "<resource group name>",
            "location": "<AzureLocation enum value name>",
            "sequence_number": "<sequence number>",
            "management_lock": {
                "name": "<lock name>",
                "lock_level": "<lock level>",
                "notes": "<notes>"
            }
        }

        Args:
            dict_ (dict): A dictionary containing resource group configuration.

        Returns:
            ResourceGroupL0Config: A fully-initialized ResourceGroupL0Config instance.
        """
        name = dict_[NAME_KEY]
        location = AzureLocation.from_full_name(dict_[LOCATION_KEY])
        sequence_number = dict_[SEQUENCE_NUMBER_KEY]

        management_lock = dict_.get(MANAGEMENT_LOCK_KEY, None)
        if management_lock:
            management_lock = ManagementLockL0Config.from_dict(dict_=dict_[MANAGEMENT_LOCK_KEY])

        return cls(
            name=name,
            location=location,
            sequence_number=sequence_number,
            management_lock=management_lock,
        )


class ResourceGroupL0(Construct, ConstructABC, metaclass=CombinedMeta):
    """
    A level 0 construct that creates and manages an Azure resource group.

    Attributes:
        resource_group (ResourceGroup): The Azure resource group.
        management_lock (ManagementLockL0 | None): The management lock applied to the resource group.
    """

    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        env: str,
        config: ResourceGroupL0Config,
    ) -> None:
        """
        Initializes the ResourceGroupL0 construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            config (ResourceGroupL0Config): The configuration for the resource group.
        """
        super().__init__(scope, id_)
        self._full_name = (
            f"{AzureResource.RESOURCE_GROUP.abbr}-{config.name}-{env}-{config.location.abbr}-{config.sequence_number}"
        )
        self._resource_group = ResourceGroup(
            self,
            f"ResourceGroup_{self._full_name}",
            name=self._full_name,
            location=config.location.full_name,
        )

        if config.management_lock:
            self._management_lock: ManagementLockL0 | None = ManagementLockL0(
                self,
                "ManagementLockL0",
                _=env,
                config=config.management_lock,
                resource_id=self._resource_group.id,
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
