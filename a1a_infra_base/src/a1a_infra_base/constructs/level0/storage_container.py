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

from a1a_infra_base.constructs.construct_abc import AttachedConstructABC, CombinedMeta, ConstructConfigABC
from a1a_infra_base.logger import setup_logger

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

        Expected format of 'config':
        {
            "name": "<storage container name>"
        }

        Args:
            dict_ (dict): A dictionary containing storage container configuration.

        Returns:
            StorageContainerL0Config: A fully-initialized StorageContainerL0Config.
        """
        name = dict_[NAME_KEY]
        return cls(name=name)


class StorageContainerL0(Construct, AttachedConstructABC[StorageContainerL0Config], metaclass=CombinedMeta):
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
        name: str,
        storage_account_id: str,
    ) -> None:
        """
        Initializes the StorageContainerL0 construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            name (str): The name of the storage container.
            storage_account_id (str): The ID of the storage account.
        """
        super().__init__(scope, id_)
        self.full_name = f"{name}"
        self._storage_container = StorageContainer(
            self,
            f"StorageContainer_{name}",
            name=name,
            storage_account_id=storage_account_id,
        )

    @property
    def storage_container(self) -> StorageContainer:
        """Gets the Azure storage container."""
        return self._storage_container

    @classmethod
    def from_config(
        cls, scope: Construct, id_: str, env: str, attach_to_resource_id: str, config: StorageContainerL0Config
    ) -> Self:
        """
        Create a StorageContainerL0 instance from a StorageContainerL0Config object.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            attach_to_resource_id (str): The resource ID to attach to.
            config (StorageContainerL0Config): The configuration object for the storage container.

        Returns:
            StorageContainerL0: A fully-initialized StorageContainerL0 instance.
        """
        return cls(
            scope,
            id_,
            _=env,
            name=config.name,
            storage_account_id=attach_to_resource_id,
        )
