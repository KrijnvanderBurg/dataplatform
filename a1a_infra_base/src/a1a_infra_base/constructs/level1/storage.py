"""
Module storage_account_locked_l1

This module defines the StorageL1 class and the StorageL1Config class,
which are responsible for creating and managing an Azure storage account with a management lock using level 0
    constructs.

Classes:
    StorageL1: A level 1 construct that creates and manages an Azure storage account with a management
                            lock.
    StorageL1Config: A configuration class for StorageL1.
"""

from dataclasses import dataclass
from typing import Any, Final, Self

from a1a_infra_base.constructs.level0.management_lock import ManagementLockL0, ManagementLockL0Config
from a1a_infra_base.constructs.level0.storage_account import StorageAccountL0, StorageAccountL0Config
from a1a_infra_base.constructs.level0.storage_container import StorageContainerL0, StorageContainerL0Config
from constructs import Construct

# Constants for dictionary keys
# root key
STORAGE_L1_KEY: Final[str] = "storage"
# attributes
STORAGE_ACCOUNT_L0_KEY: Final[str] = "storage_account"
MANAGEMENT_LOCK_L0_KEY: Final[str] = "management_lock"
STORAGE_CONTAINERS_L0_KEY: Final[str] = "storage_containers"


@dataclass
class StorageL1Config:
    """
    A configuration class for StorageL1.

    Attributes:
        storage_account_l0 (StorageAccountL0Config): The configuration for the storage account.
        management_lock_l0 (ManagementLockL0Config): The configuration for the management lock.
        storage_containers_l0 (list[StorageContainerL0Config]): The configuration for the storage containers.
    """

    storage_account_l0: StorageAccountL0Config
    management_lock_l0: ManagementLockL0Config = ManagementLockL0Config(lock_level="CanNotDelete")
    storage_containers_l0: list[StorageContainerL0Config] | None = None

    @classmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Create a StorageL1Config by unpacking parameters from a configuration dictionary.

        Args:
            dict_ (dict[str, Any]): A dictionary containing storage account, management lock, and storage containers
            configuration.

        Returns:
            StorageL1Config: A fully-initialized StorageL1Config.
        """
        storage_account_l0 = StorageAccountL0Config.from_dict(dict_[STORAGE_ACCOUNT_L0_KEY])
        management_lock_l0 = (
            ManagementLockL0Config.from_dict(dict_[MANAGEMENT_LOCK_L0_KEY])
            if MANAGEMENT_LOCK_L0_KEY in dict_
            else cls.management_lock_l0
        )
        storage_containers_l0 = [
            StorageContainerL0Config.from_dict(container) for container in dict_.get(STORAGE_CONTAINERS_L0_KEY, [])
        ]

        return cls(
            storage_account_l0=storage_account_l0,
            management_lock_l0=management_lock_l0,
            storage_containers_l0=storage_containers_l0,
        )


class StorageL1(Construct):
    """
    A level 1 construct that creates and manages an Azure storage account with a management lock and storage containers.

    Attributes:
        storage_account (StorageAccountL0): The Azure storage account.
        management_lock (ManagementLockL0): The management lock applied to the storage account.
        storage_containers (list[StorageContainerL0]): The Azure storage containers.
    """

    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        env: str,
        config: StorageL1Config,
        resource_group_name: str,
    ) -> None:
        """
        Initializes the StorageL1 construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            config (StorageL1Config): The configuration for the storage account, management lock, and storage containers.
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

        self._management_lock = ManagementLockL0(
            self,
            "ManagementLockL0",
            _=env,
            config=config.management_lock_l0,
            resource_id=self._storage_account_l0.storage_account.id,
            resource_name=self._storage_account_l0.full_name,
        )

        self._storage_containers = [
            StorageContainerL0(
                self,
                f"StorageContainerL0_{container.name}",
                _=env,
                config=container,
                storage_account_id=self._storage_account_l0.storage_account.id,
            )
            for container in config.storage_containers_l0 or []
        ]

    @property
    def storage_account(self) -> StorageAccountL0:
        """Gets the Azure storage account."""
        return self._storage_account_l0

    @property
    def management_lock(self) -> ManagementLockL0:
        """Gets the management lock applied to the storage account."""
        return self._management_lock

    @property
    def storage_containers(self) -> list[StorageContainerL0]:
        """Gets the Azure storage containers."""
        return self._storage_containers
