"""
Module terraform_backend

This module defines the TerraformBackendL0 class, which creates a resource group and a locked storage account.

Classes:
    TerraformBackendL0: A construct that creates a resource group and a locked storage account.
    TerraformBackendL2Config: A configuration class for TerraformBackendL0.
"""

import logging
from dataclasses import dataclass
from typing import Any, Final, Self

from a1a_infra_base.constructs.ABC import CombinedMeta, ConstructConfigABC
from a1a_infra_base.constructs.level0.resource_group import ResourceGroupL0, ResourceGroupL0Config
from a1a_infra_base.constructs.level0.management_lock import ManagementLockL0, ManagementLockL0Config
from a1a_infra_base.constructs.level1.storage import STORAGE_L1_KEY, StorageL1, StorageL1Config
from a1a_infra_base.logger import setup_logger
from constructs import Construct

logger: logging.Logger = setup_logger(__name__)

# Constants for dictionary keys
# root key
TERRAFORM_BACKEND_L2_KEY: Final[str] = "terraform_backend_l2"
# attributes
RESOURCE_GROUP_LOCKED_L1_KEY: Final[str] = "resource_group_locked_l1"


@dataclass
class TerraformBackendL2Config(ConstructConfigABC):
    """
    A configuration class for TerraformBackendL0.

    Attributes:
        resource_group_config (ResourceGroupLockedL1Config): The configuration for the resource group.
        storage_account_with_containers_l2 (StorageL1Config): The configuration for the storage account.
    """

    resource_group_secure_l1: ResourceGroupSecureL1Config
    storage_l1: StorageL1Config

    @classmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Create a TerraformBackendL2Config by unpacking parameters from a configuration dictionary.

        Args:
            dict_ (dict): A dictionary containing the configuration.

        Returns:
            TerraformBackendL2Config: A fully-initialized TerraformBackendL2Config.
        """
        resource_group_locked_l1 = ResourceGroupSecureL1Config.from_dict(dict_[RESOURCE_GROUP_LOCKED_L1_KEY])
        storage_l1 = StorageL1Config.from_dict(dict_[STORAGE_L1_KEY])

        return cls(
            resource_group_secure_l1=resource_group_locked_l1,
            storage_l1=storage_l1,
        )


class TerraformBackendL2(Construct, metaclass=CombinedMeta):
    """
    A level 1 construct that creates and manages a Terraform backend.

    Attributes:
        resource_group (ResourceGroupL0): The Azure resource group.
        storage_account (StorageAccountL0): The Azure storage account.
    """

    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        env: str,
        config: TerraformBackendL2Config,
    ) -> None:
        """
        Initializes the TerraformBackendL0 construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            config (TerraformBackendL2Config): The configuration for the Terraform backend.
        """
        super().__init__(scope, id_)

        # Create the resource group
        self.resource_group_l0 = ResourceGroupSecureL1(
            self,
            "ResourceGroupSecureL1",
            env=env,
            config=config.resource_group_secure_l1,
        )

        # Create the storage account
        self.storage_account_l0 = StorageL1(
            self,
            "StorageL1",
            env=env,
            config=config.storage_l1,
            resource_group_name=self.resource_group_l0.resource_group.name,
        )
