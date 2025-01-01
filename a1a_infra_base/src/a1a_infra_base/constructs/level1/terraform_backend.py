"""
Module terraform_backend

This module defines the TerraformBackendL0 class, which creates a resource group and a locked storage account.

Classes:
    TerraformBackendL0: A construct that creates a resource group and a locked storage account.
    TerraformBackendL1Config: A configuration class for TerraformBackendL0.
"""

import logging
from dataclasses import dataclass
from typing import Any, Final, Self

from constructs import Construct

from a1a_infra_base.constructs.construct_abc import CombinedMeta, ConstructConfigABC
from a1a_infra_base.constructs.level0.resource_group import ResourceGroupL0, ResourceGroupL0Config
from a1a_infra_base.constructs.level0.storage_account import StorageAccountL0, StorageAccountL0Config
from a1a_infra_base.logger import setup_logger

logger: logging.Logger = setup_logger(__name__)

# Constants for dictionary keys
RESOURCE_GROUP_L0_KEY: Final[str] = "resource_group_l0"
STORAGE_ACCOUNT_L0_KEY: Final[str] = "storage_account_l0"


@dataclass
class TerraformBackendL1Config(ConstructConfigABC):
    """
    A configuration class for TerraformBackendL0.

    Attributes:
        resource_group_config (ResourceGroupL0Config): The configuration for the resource group.
        storage_account_config (StorageAccountL0Config): The configuration for the storage account.
    """

    resource_group_config: ResourceGroupL0Config
    storage_account_config: StorageAccountL0Config

    @classmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Create a TerraformBackendL1Config by unpacking parameters from a configuration dictionary.

        Args:
            dict_ (dict): A dictionary containing the configuration.

        Returns:
            TerraformBackendL1Config: A fully-initialized TerraformBackendL1Config.
        """
        resource_group_config = ResourceGroupL0Config.from_dict(dict_[RESOURCE_GROUP_L0_KEY])
        storage_account_config = StorageAccountL0Config.from_dict(dict_[STORAGE_ACCOUNT_L0_KEY])

        return cls(resource_group_config=resource_group_config, storage_account_config=storage_account_config)


class TerraformBackendL1(Construct, metaclass=CombinedMeta):
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
        config: TerraformBackendL1Config,
    ) -> None:
        """
        Initializes the TerraformBackendL0 construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            config (TerraformBackendL1Config): The configuration for the Terraform backend.
        """
        super().__init__(scope, id_)

        # Create the resource group
        self.resource_group_l0 = ResourceGroupL0(
            self,
            "ResourceGroupL0",
            env=env,
            config=config.resource_group_config,
        )

        # Create the storage account
        self.storage_account_l0 = StorageAccountL0(
            self,
            "StorageAccountL0",
            env=env,
            config=config.storage_account_config,
            resource_group_name=self.resource_group_l0.resource_group.name,
        )
