"""
Module terraform_backend

This module defines the TerraformBackendL0 class, which creates a resource group and a locked storage account.

Classes:
    TerraformBackendL0: A construct that creates a resource group and a locked storage account.
    LakeHouseL2Config: A configuration class for TerraformBackendL0.
"""

import logging
from dataclasses import dataclass
from typing import Any, Final, Self

from a1a_infra_base.constructs.construct_abc import CombinedMeta, ConstructConfigABC
from a1a_infra_base.constructs.level1.resource_group_secure import (
    RESOURCE_GROUP_SECURE_L1_KEY,
    ResourceGroupSecureL1,
    ResourceGroupSecureL1Config,
)
from a1a_infra_base.constructs.level1.storage import STORAGE_L1_KEY, StorageL1, StorageL1Config
from a1a_infra_base.logger import setup_logger
from constructs import Construct

logger: logging.Logger = setup_logger(__name__)

# Constants for dictionary keys
# root key
DATA_LAKE_L2_KEY: Final[str] = "data_lake"
# attributes
STORAGES_KEY: Final[str] = "storages"


@dataclass
class DataLakeL2Config(ConstructConfigABC):
    """
    A configuration class for TerraformBackendL0.

    Attributes:
        resource_group_l0_config (ResourceGroupSecureL1Config): The configuration for the resource group.
        data_lake_l1_config (StorageL1Config): The configuration for the storage account.
    """

    resource_group_secure_l1_config: ResourceGroupSecureL1Config
    storage_l1_configs: list[StorageL1Config]

    @classmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Create a LakeHouseL2Config by unpacking parameters from a configuration dictionary.

        Args:
            dict_ (dict): A dictionary containing the configuration.

        Returns:
            LakeHouseL2Config: A fully-initialized LakeHouseL2Config.
        """
        resource_group_secure_l1_config = ResourceGroupSecureL1Config.from_dict(dict_[RESOURCE_GROUP_SECURE_L1_KEY])

        storage_l1_configs: list[StorageL1Config] = []
        for storage in dict_[STORAGES_KEY]:
            storage_l1_configs.append(StorageL1Config.from_dict(storage[STORAGE_L1_KEY]))

        return cls(
            resource_group_secure_l1_config=resource_group_secure_l1_config, storage_l1_configs=storage_l1_configs
        )


class DataLakeL2(Construct, metaclass=CombinedMeta):
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
        config: DataLakeL2Config,
    ) -> None:
        """
        Initializes the TerraformBackendL0 construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            config (LakeHouseL2Config): The configuration for the Terraform backend.
        """
        super().__init__(scope, id_)

        self._resource_group_secure_l1 = ResourceGroupSecureL1(
            self,
            "ResourceGroupSecureL1",
            env=env,
            config=config.resource_group_secure_l1_config,
        )

        storages_l1: list[StorageL1] = []
        for storage_l1_config in config.storage_l1_configs:
            storage_l1 = StorageL1(
                self,
                "StorageL1",
                env=env,
                config=storage_l1_config,
                resource_group_name=self._resource_group_secure_l1.resource_group.name,
            )
            storages_l1.append(storage_l1)
        self._storages_l1 = storages_l1

    @property
    def resource_group_secure_l1(self) -> ResourceGroupSecureL1:
        return self._resource_group_secure_l1

    @property
    def storages_l1(self) -> list[StorageL1]:
        return self._storages_l1
