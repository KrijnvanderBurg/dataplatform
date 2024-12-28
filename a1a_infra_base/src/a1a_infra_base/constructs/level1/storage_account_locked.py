"""
Module storage_account_locked

This module defines the StorageAccountLockedL1 class and the StorageAccountLockedL1Config class,
which are responsible for creating and managing a locked Azure storage account with specific configurations.

Classes:
    StorageAccountLockedL1: A level 1 construct that creates and manages a locked Azure storage account.
    StorageAccountLockedL1Config: A configuration class for StorageAccountLockedL1.
"""

from dataclasses import dataclass
from typing import Any, Final, Self

from constructs import Construct

from a1a_infra_base.constructs.level0.management_lock import ManagementLockL0, ManagementLockL0Config
from a1a_infra_base.constructs.level0.resource_group import ResourceGroupL0
from a1a_infra_base.constructs.level0.storage_account import StorageAccountL0, StorageAccountL0Config

# Constants for dictionary keys
MANAGEMENT_LOCK_KEY: Final[str] = "management_lock"


@dataclass
class StorageAccountLockedL1Config:
    """
    A configuration class for StorageAccountLockedL1.

    This class is responsible for unpacking parameters from a configuration dictionary.
    """

    env: str
    storage_account_config: StorageAccountL0Config
    management_lock_config: ManagementLockL0Config

    @classmethod
    def from_config(cls, env: str, config: dict[str, Any]) -> Self:
        """
        Create a StorageAccountLockedConfig by unpacking parameters from a configuration dictionary.

        Expected format of 'config':
        {
            "name": "<storage account name>",
            "location": "<AzureLocation enum value name>",
            "sequence_number": "<sequence number>",
            "resource_group_name": "<resource group name>",
            "account_replication_type": "<replication type>",
            "account_kind": "<account kind>",
            "account_tier": "<account tier>",
            "cross_tenant_replication_enabled": <bool>,
            "access_tier": "<access tier>",
            "shared_access_key_enabled": <bool>,
            "public_network_access_enabled": <bool>,
            "is_hns_enabled": <bool>,
            "local_user_enabled": <bool>,
            "infrastructure_encryption_enabled": <bool>,
            "sftp_enabled": <bool>,
            "blob_properties": {
                "delete_retention_policy": {
                    "delete_retention_days": <int>
                }
            },
            "management_lock": {
                "lock_level": "<lock level>"
                "notes": "<notes>"
            }
        }

        Args:
            env (str): The environment name.
            config (dict): A dictionary containing storage account configuration.

        Returns:
            StorageAccountLockedL1Config: An instance of StorageAccountLockedL1Config.
        """
        storage_account_config = StorageAccountL0Config.from_config(env=env, config=config)
        management_lock_config = ManagementLockL0Config.from_config(
            env=env, name=storage_account_config.full_name, config=config[MANAGEMENT_LOCK_KEY]
        )

        return cls(
            env=env, storage_account_config=storage_account_config, management_lock_config=management_lock_config
        )


class StorageAccountLockedL1(Construct):
    """
    A level 1 construct that creates and manages a locked Azure storage account.

    Attributes:
        storage_account (StorageAccountL0): The Azure storage account.
        management_lock (ManagementLockL0): The management lock applied to the storage account.
    """

    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        config: StorageAccountLockedL1Config,
        resource_group_l0: ResourceGroupL0,
    ) -> None:
        """
        Initializes the StorageAccountLockedL1 construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            config (StorageAccountLockedL1Config): The configuration for the storage account.
            resource_group_l0 (ResourceGroupL0): The resource group level 0 construct.
        """
        super().__init__(scope, id_)

        self._storage_account = StorageAccountL0(
            self,
            "StorageAccountL0",
            config=config.storage_account_config,
            resource_group_l0=resource_group_l0,
        )

        self._management_lock = ManagementLockL0(
            self,
            "ManagementLockL0",
            config=config.management_lock_config,
            resource_id=self.storage_account.storage_account.id,
        )

    @property
    def storage_account(self) -> StorageAccountL0:
        """Gets the Azure storage account."""
        return self._storage_account

    @property
    def management_lock(self) -> ManagementLockL0:
        """Gets the management lock applied to the storage account."""
        return self._management_lock
