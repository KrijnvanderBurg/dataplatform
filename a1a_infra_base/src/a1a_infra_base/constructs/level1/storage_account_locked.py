"""
Module storage_account_locked_l1

This module defines the StorageAccountLockedL1 class and the StorageAccountLockedL1Config class,
which are responsible for creating and managing an Azure storage account with a management lock using level 0
    constructs.

Classes:
    StorageAccountLockedL1: A level 1 construct that creates and manages an Azure storage account with a management
                            lock.
    StorageAccountLockedL1Config: A configuration class for StorageAccountLockedL1.
"""

from dataclasses import dataclass
from typing import Any, Final, Self

from a1a_infra_base.constructs.level0.management_lock import ManagementLockL0, ManagementLockL0Config
from a1a_infra_base.constructs.level0.storage_account import StorageAccountL0, StorageAccountL0Config
from constructs import Construct

# Constants for dictionary keys
STORAGE_ACCOUNT_L0_KEY: Final[str] = "storage_account_l0"
MANAGEMENT_LOCK_L0_KEY: Final[str] = "management_lock_l0"


@dataclass
class StorageAccountLockedL1Config:
    """
    A configuration class for StorageAccountLockedL1.

    Attributes:
        storage_account_l0 (StorageAccountL0Config): The configuration for the storage account.
        management_lock_l0 (ManagementLockL0Config): The configuration for the management lock.
    """

    storage_account_l0: StorageAccountL0Config
    management_lock_l0: ManagementLockL0Config | None = None

    @classmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Create a StorageAccountLockedL1Config by unpacking parameters from a configuration dictionary.

        Args:
            dict_ (dict[str, Any]): A dictionary containing storage account and management lock configuration.

        Returns:
            StorageAccountLockedL1Config: A fully-initialized StorageAccountLockedL1Config.
        """
        storage_account_l0 = StorageAccountL0Config.from_dict(dict_[STORAGE_ACCOUNT_L0_KEY])
        management_lock_l0 = (
            ManagementLockL0Config.from_dict(dict_[MANAGEMENT_LOCK_L0_KEY]) if MANAGEMENT_LOCK_L0_KEY in dict_ else None
        )

        return cls(
            storage_account_l0=storage_account_l0,
            management_lock_l0=management_lock_l0,
        )


class StorageAccountLockedL1(Construct):
    """
    A level 1 construct that creates and manages an Azure storage account with a management lock.

    Attributes:
        storage_account (StorageAccountL0): The Azure storage account.
        management_lock (ManagementLockL0): The management lock applied to the storage account.
    """

    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        env: str,
        config: StorageAccountLockedL1Config,
        resource_group_name: str,
    ) -> None:
        """
        Initializes the StorageAccountLockedL1 construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            config (StorageAccountLockedL1Config): The configuration for the storage account and management lock.
            resource_group_name (str): The name of the resource group.
        """
        super().__init__(scope, id_)

        self._storage_account_l0 = StorageAccountL0(
            self,
            f"StorageAccountL0_{id_}",
            env=env,
            config=config.storage_account_l0,
            resource_group_name=resource_group_name,
        )

        if config.management_lock_l0:
            self._management_lock: ManagementLockL0 | None = ManagementLockL0(
                self,
                "ManagementLockL0",
                _=env,
                config=config.management_lock_l0,
                resource_id=self._storage_account_l0.storage_account.id,
                resource_name=self._storage_account_l0.full_name,
            )
        else:
            self._management_lock = None

    @property
    def storage_account(self) -> StorageAccountL0:
        """Gets the Azure storage account."""
        return self._storage_account_l0

    @property
    def management_lock(self) -> ManagementLockL0 | None:
        """Gets the management lock applied to the storage account."""
        return self._management_lock
