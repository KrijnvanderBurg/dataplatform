"""
Module storage_container

This module defines the StorageContainerL0 class, which is responsible for creating
and managing an Azure storage container with specific configurations.

Classes:
    StorageContainerL0: A level 0 construct that creates and manages an Azure storage container.
"""

from typing import Final

from cdktf_cdktf_provider_azurerm.storage_container import StorageContainer
from constructs import Construct

from a1a_infra_base.constructs.level0.storage_account import StorageAccountL0

# Constants for dictionary keys
NAME_KEY: Final[str] = "name"
STORAGE_ACCOUNT_KEY: Final[str] = "storage_account"
CONTAINER_ACCESS_TYPE_KEY: Final[str] = "container_access_type"


class StorageContainerL0(Construct):
    """
    A level 0 construct that creates and manages an Azure storage container.

    Attributes:
        storage_container (StorageContainer): The Azure storage container.
    """

    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        _: str,  # env: str, unused thus _. Kept to maintain consistency and available for future use.
        name: str,
        storage_account_l0: StorageAccountL0,
        container_access_type: str,
    ) -> None:
        """
        Initializes the StorageContainerL0 construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            name (str): The name of the storage container.
            storage_account_l0 (StorageAccountL0): The storage account level 0 construct.
            container_access_type (str): The access type of the storage container.
        """
        super().__init__(scope, id_)
        self._storage_container = StorageContainer(
            self,
            f"{storage_account_l0.storage_account.id}_{name}",
            name=name,
            storage_account_id=storage_account_l0.storage_account.id,
            container_access_type=container_access_type,
        )

    @property
    def storage_container(self) -> StorageContainer:
        """Gets the Azure storage container."""
        return self._storage_container

    @classmethod
    def from_config(
        cls, scope: Construct, id_: str, env: str, config: dict, storage_account_l0: StorageAccountL0
    ) -> "StorageContainerL0":
        """
        Create a StorageContainerL0 construct by unpacking parameters from a configuration dictionary.

        Expected format of 'config':
        {
            "name": "<storage container name>",
            "container_access_type": "<access type>"
        }

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            config (dict): A dictionary containing storage container configuration.
            storage_account_l0 (StorageAccountL0): The storage account level 0 construct.

        Returns:
            StorageContainerL0: A fully-initialized StorageContainerL0 construct.
        """
        name = config[NAME_KEY]
        container_access_type = config[CONTAINER_ACCESS_TYPE_KEY]

        return cls(
            scope,
            id_,
            _=env,
            name=name,
            storage_account_l0=storage_account_l0,
            container_access_type=container_access_type,
        )
