"""
Module resource_group

This module defines the ResourceGroupLockedL1 class and the ResourceGroupLockedL1Config class,
which are responsible for creating and managing an Azure resource group with specific configurations.

Classes:
    ResourceGroupLockedL1: A level 0 construct that creates and manages an Azure resource group.
    ResourceGroupLockedL1Config: A configuration class for ResourceGroupLockedL1.
"""

import logging
from dataclasses import dataclass
from typing import Any, Final, Self

from cdktf_cdktf_provider_azurerm.resource_group import ResourceGroup

from a1a_infra_base.constants import AzureResource
from a1a_infra_base.constructs.construct_abc import CombinedMeta, ConstructABC, ConstructConfigABC
from a1a_infra_base.constructs.level0.management_lock import ManagementLockL0, ManagementLockL0Config
from a1a_infra_base.constructs.level0.resource_group import ResourceGroupL0Config
from a1a_infra_base.logger import setup_logger
from constructs import Construct

logger: logging.Logger = setup_logger(__name__)

# Constants for dictionary keys
RESOURCE_GROUP_L0_KEY: Final[str] = "resource_group_l0"
MANAGEMENT_LOCK_L0_KEY: Final[str] = "management_lock_l0"


@dataclass
class ResourceGroupLockedL1Config(ConstructConfigABC):
    """
    A configuration class for ResourceGroupLockedL1.

    Attributes:
        name (str): The name of the resource group.
        location (AzureLocation): The Azure location.
        sequence_number (str): The sequence number.
        management_lock_l0 (ManagementLockL0Config | None): The management lock configuration.
    """

    resource_group_l0: ResourceGroupL0Config
    management_lock_l0: ManagementLockL0Config

    @classmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Create a ResourceGroupLockedL1Config instance by unpacking parameters from a configuration dictionary.

        The expected format of 'dict_' is:
        {

        }

        Args:
            dict_ (dict[str, Any]): A dictionary containing resource group configuration.

        Returns:
            ResourceGroupLockedL1Config: A fully-initialized ResourceGroupLockedL1Config instance.
        """

        resource_group_l0 = ResourceGroupL0Config.from_dict(dict_[RESOURCE_GROUP_L0_KEY])
        management_lock_l0 = ManagementLockL0Config.from_dict(dict_[MANAGEMENT_LOCK_L0_KEY])

        return cls(
            resource_group_l0=resource_group_l0,
            management_lock_l0=management_lock_l0,
        )


class ResourceGroupLockedL1(Construct, ConstructABC, metaclass=CombinedMeta):
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
        config: ResourceGroupLockedL1Config,
    ) -> None:
        """
        Initializes the ResourceGroupLockedL1 construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            config (ResourceGroupLockedL1Config): The configuration for the resource group.
        """
        super().__init__(scope, id_)
        self.full_name = (
            f"{AzureResource.RESOURCE_GROUP.abbr}-"
            f"{config.resource_group_l0.name}-"
            f"{env}-"
            f"{config.resource_group_l0.location.abbr}-"
            f"{config.resource_group_l0.sequence_number}"
        )

        self._resource_group = ResourceGroup(
            self,
            f"ResourceGroup_{self.full_name}",
            name=self.full_name,
            location=config.resource_group_l0.location.full_name,
        )

        self._management_lock = ManagementLockL0(
            self,
            "ManagementLockL0",
            _=env,
            config=config.management_lock_l0,
            resource_id=self.resource_group.id,
            resource_name=self.full_name,
        )

    @property
    def resource_group(self) -> ResourceGroup:
        """Gets the Azure resource group."""
        return self._resource_group
