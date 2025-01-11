"""
Module terraform_backend

This module defines the TerraformBackendL0 class, which creates a resource group and a locked storage account.

Classes:
    TerraformBackendL0: A construct that creates a resource group and a locked storage account.
    TerraformBackendL3Config: A configuration class for TerraformBackendL0.
"""

import logging
from dataclasses import dataclass
from typing import Any, Final, Self

from a1a_infra_base.constructs.construct_abc import CombinedMeta, ConstructConfigABC
from a1a_infra_base.constructs.level1.resource_group_locked import ResourceGroupLockedL1, ResourceGroupLockedL1Config
from a1a_infra_base.constructs.level2.storage_account_with_containers import (
    StorageAccountWithContainersL2,
    StorageAccountWithContainersL2Config,
)
from a1a_infra_base.logger import setup_logger
from constructs import Construct

logger: logging.Logger = setup_logger(__name__)

# Constants for dictionary keys
RESOURCE_GROUP_LOCKED_L1_KEY: Final[str] = "resource_group_locked_l1"
STORAGE_ACCOUNT_WITH_CONTAINERS_L2_KEY: Final[str] = "storage_account_with_containers_l2"


@dataclass
class TerraformBackendL3Config(ConstructConfigABC):
    """
    A configuration class for TerraformBackendL0.

    Attributes:
        resource_group_config (ResourceGroupLockedL1Config): The configuration for the resource group.
        storage_account_with_containers_l2 (StorageAccountWithContainersL2Config): The configuration for the storage account.
    """

    resource_group_locked_l1: ResourceGroupLockedL1Config
    storage_account_with_containers_l2: StorageAccountWithContainersL2Config

    @classmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Create a TerraformBackendL3Config by unpacking parameters from a configuration dictionary.

        Args:
            dict_ (dict): A dictionary containing the configuration.

        Returns:
            TerraformBackendL3Config: A fully-initialized TerraformBackendL3Config.
        """
        resource_group_locked_l1 = ResourceGroupLockedL1Config.from_dict(dict_[RESOURCE_GROUP_LOCKED_L1_KEY])
        storage_account_with_containers_l2 = StorageAccountWithContainersL2Config.from_dict(
            dict_[STORAGE_ACCOUNT_WITH_CONTAINERS_L2_KEY]
        )

        return cls(
            resource_group_locked_l1=resource_group_locked_l1,
            storage_account_with_containers_l2=storage_account_with_containers_l2,
        )


class TerraformBackendL3(Construct, metaclass=CombinedMeta):
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
        config: TerraformBackendL3Config,
    ) -> None:
        """
        Initializes the TerraformBackendL0 construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            config (TerraformBackendL3Config): The configuration for the Terraform backend.
        """
        super().__init__(scope, id_)

        # Create the resource group
        self.resource_group_l0 = ResourceGroupLockedL1(
            self,
            "ResourceGroupL0",
            env=env,
            config=config.resource_group_locked_l1,
        )

        # Create the storage account
        self.storage_account_l0 = StorageAccountWithContainersL2(
            self,
            "StorageAccountL0",
            env=env,
            config=config.storage_account_with_containers_l2,
            resource_group_name=self.resource_group_l0.resource_group.name,
        )
