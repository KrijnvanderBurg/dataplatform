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

from a1a_infra_base.constructs.ABC import CombinedMeta, ConstructABC, ConstructConfigABC
from a1a_infra_base.logger import setup_logger
from constructs import Construct

logger: logging.Logger = setup_logger(__name__)

# Constants for dictionary keys
NAME_KEY: Final[str] = "name"


@dataclass
class StorageContainerL0Config(ConstructConfigABC):
    """
    A configuration class for StorageContainerL0.

    Attributes:
        name (str): The name of the storage container.
    """

    name: str

    @property
    def full_name(self) -> str:
        """Generates the full name for the storage container."""
        return f"{self.name}"

    @classmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Create a StorageContainerL0Config by unpacking parameters from a configuration dictionary.

        Expected format of 'dict_':
        {
            "name": "<storage container name>"
        }

        Args:
            dict_ (dict[str, Any]): A dictionary containing storage container configuration.

        Returns:
            StorageContainerL0Config: A fully-initialized StorageContainerL0Config.
        """
        name = dict_[NAME_KEY]
        return cls(name=name)


class StorageContainerL0(Construct, ConstructABC, metaclass=CombinedMeta):
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
        _: str,  # unused env parameter; only present for consistency and to match signature
        config: StorageContainerL0Config,
        storage_account_id: str,
    ) -> None:
        """
        Initializes the StorageContainerL0 construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            config (StorageContainerL0Config): The configuration for the storage container.
            storage_account_id (str): The ID of the storage account.
        """
        super().__init__(scope, id_)

        self.full_name = f"{config.name}"
        self._storage_container = StorageContainer(
            self,
            f"StorageContainer_{config.name}",
            name=config.name,
            storage_account_id=storage_account_id,
        )
