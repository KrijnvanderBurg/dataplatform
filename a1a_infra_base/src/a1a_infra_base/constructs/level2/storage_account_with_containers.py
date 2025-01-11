"""
Module storage_account_with_containers_l2

This module defines the StorageAccountWithContainersL2 class and the StorageAccountWithContainersL2Config class,
which are responsible for creating and managing an Azure storage account with a management lock and storage containers
using level 1 constructs.

Classes:
    StorageAccountWithContainersL2: A level 2 construct that creates and manages an Azure storage account with a
    management lock and storage containers.
    StorageAccountWithContainersL2Config: A configuration class for StorageAccountWithContainersL2.
"""

from dataclasses import dataclass
from typing import Any, Final, Self

from a1a_infra_base.constructs.level0.storage_container import StorageContainerL0, StorageContainerL0Config
from a1a_infra_base.constructs.level1.storage_account_locked import (
    StorageAccountLockedL1,
    StorageAccountLockedL1Config,
)
from constructs import Construct

# Constants for dictionary keys
STORAGE_ACCOUNT_LOCKED_L1_KEY: Final[str] = "storage_account_locked_l1"
STORAGE_CONTAINERS_L0_KEY: Final[str] = "storage_containers_l0"


@dataclass
class StorageAccountWithContainersL2Config:
    """
    A configuration class for StorageAccountWithContainersL2.

    Attributes:
        storage_account_locked_l1 (StorageAccountLockedL1Config): The configuration for the storage account with
        management lock.
        storage_containers_l0 (list[StorageContainerL0Config]): The configuration for the storage containers.
    """

    storage_account_locked_l1: StorageAccountLockedL1Config
    storage_containers_l0: list[StorageContainerL0Config]

    @classmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Create a StorageAccountWithContainersL2Config by unpacking parameters from a configuration dictionary.

        Args:
            dict_ (dict[str, Any]): A dictionary containing storage account, management lock, and storage containers
            configuration.

        Returns:
            StorageAccountWithContainersL2Config: A fully-initialized StorageAccountWithContainersL2Config.
        """
        storage_account_locked_l1 = StorageAccountLockedL1Config.from_dict(dict_[STORAGE_ACCOUNT_LOCKED_L1_KEY])

        storage_containers_l0 = []
        for container in dict_[STORAGE_CONTAINERS_L0_KEY]:
            storage_containers_l0.append(StorageContainerL0Config.from_dict(container))

        return cls(
            storage_account_locked_l1=storage_account_locked_l1,
            storage_containers_l0=storage_containers_l0,
        )


class StorageAccountWithContainersL2(Construct):
    """
    A level 2 construct that creates and manages an Azure storage account with a management lock and storage containers.

    Attributes:
        storage_account (StorageAccountLockedL1): The Azure storage account with a management lock.
    """

    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        env: str,
        config: StorageAccountWithContainersL2Config,
        resource_group_name: str,
    ) -> None:
        """
        Initializes the StorageAccountWithContainersL2 construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            config (StorageAccountWithContainersL2Config): The configuration for the storage account, management lock,
            and storage containers.
            resource_group_name (str): The name of the resource group.
        """
        super().__init__(scope, id_)

        self._storage_account_locked_l1 = StorageAccountLockedL1(
            self,
            f"StorageAccountLockedL1_{id_}",
            env=env,
            config=config.storage_account_locked_l1,
            resource_group_name=resource_group_name,
        )

        for container in config.storage_containers_l0:
            StorageContainerL0(
                self,
                f"StorageContainerL0_{container.name}",
                _=env,
                config=container,
                storage_account_id=self._storage_account_locked_l1.storage_account.storage_account.id,
            )

    @property
    def storage_account(self) -> StorageAccountLockedL1:
        """Gets the Azure storage account with a management lock."""
        return self._storage_account_locked_l1
