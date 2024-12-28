"""
Module storage_container

This module defines the StorageContainerL0 class and the StorageContainerL0Config class,
which are responsible for creating and managing an Azure storage container with specific configurations.

Classes:
    StorageContainerL0: A level 0 construct that creates and manages an Azure storage container.
    StorageContainerL0Config: A configuration class for StorageContainerL0.
"""

import logging
from dataclasses import dataclass
from typing import Any, Final, Self

from cdktf_cdktf_provider_azurerm.storage_container import StorageContainer
from constructs import Construct

from a1a_infra_base.logger import setup_logger

logger: logging.Logger = setup_logger(__name__)

# Constants for dictionary keys
NAME_KEY: Final[str] = "name"


@dataclass
class StorageContainerL0Config:
    """
    A configuration class for StorageContainerL0.

    Attributes:
        name (str): The name of the storage container.
        container_access_type (str): The access type of the storage container.
    """

    name: str

    @property
    def full_name(self) -> str:
        """Generates the full name for the storage container."""
        return f"{self.name}"

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> Self:
        """
        Create a StorageContainerL0Config by unpacking parameters from a configuration dictionary.

        Expected format of 'config':
        {
            "name": "<storage container name>",
            "container_access_type": "<access type>"
        }

        Args:
            config (dict): A dictionary containing storage container configuration.

        Returns:
            StorageContainerL0Config: A fully-initialized StorageContainerL0Config.
        """
        name = config[NAME_KEY]
        return cls(name=name)


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
        config: StorageContainerL0Config,
        storage_account_id: str,
    ) -> None:
        """
        Initializes the StorageContainerL0 construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            config (StorageContainerL0Config): The configuration for the storage container.
            storage_account_l0 (StorageAccountL0): The storage account level 0 construct.
        """
        super().__init__(scope, id_)
        self._storage_container = StorageContainer(
            self,
            f"StorageContainer_{config.full_name}",
            name=config.name,
            storage_account_id=storage_account_id,
        )

    @property
    def storage_container(self) -> StorageContainer:
        """Gets the Azure storage container."""
        return self._storage_container
