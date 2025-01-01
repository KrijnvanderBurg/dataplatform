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
        resource_group_config: ResourceGroupL0Config,
        storage_account_config: StorageAccountL0Config,
    ) -> None:
        """
        Initializes the TerraformBackendL0 construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            resource_group_config (ResourceGroupL0Config): The configuration for the resource group.
            storage_account_config (StorageAccountL0Config): The configuration for the storage account.
        """
        super().__init__(scope, id_)

        # Create the resource group
        self.resource_group_l0 = ResourceGroupL0(
            self,
            "ResourceGroupL0",
            env=env,
            name=resource_group_config.name,
            location=resource_group_config.location,
            sequence_number=resource_group_config.sequence_number,
            management_lock=resource_group_config.management_lock,
        )

        # Create the storage account
        self.storage_account_l0 = StorageAccountL0(
            self,
            "StorageAccountL0",
            env=env,
            name=storage_account_config.name,
            location=storage_account_config.location,
            resource_group_name=self.resource_group_l0.resource_group.name,
            sequence_number=storage_account_config.sequence_number,
            account_replication_type=storage_account_config.account_replication_type,
            account_kind=storage_account_config.account_kind,
            account_tier=storage_account_config.account_tier,
            cross_tenant_replication_enabled=storage_account_config.cross_tenant_replication_enabled,
            access_tier=storage_account_config.access_tier,
            shared_access_key_enabled=storage_account_config.shared_access_key_enabled,
            public_network_access_enabled=storage_account_config.public_network_access_enabled,
            is_hns_enabled=storage_account_config.is_hns_enabled,
            local_user_enabled=storage_account_config.local_user_enabled,
            infrastructure_encryption_enabled=storage_account_config.infrastructure_encryption_enabled,
            sftp_enabled=storage_account_config.sftp_enabled,
            blob_properties=storage_account_config.blob_properties,
            containers=storage_account_config.containers,
            management_lock=storage_account_config.management_lock,
        )
