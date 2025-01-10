"""
Module terraform_backend

This module defines the TerraformBackendL0 class, which creates a resource group and a locked storage account.

Classes:
    TerraformBackendL0: A construct that creates a resource group and a locked storage account.
    MedallionDataLakeL2Config: A configuration class for TerraformBackendL0.
"""

import logging
from dataclasses import dataclass
from typing import Any, Final, Self

from a1a_infra_base.constructs.construct_abc import CombinedMeta, ConstructConfigABC
from a1a_infra_base.constructs.level0.resource_group import ResourceGroupL0, ResourceGroupL0Config
from a1a_infra_base.constructs.level1.datalake import DataLakeL1, DataLakeL1Config
from a1a_infra_base.logger import setup_logger
from constructs import Construct

logger: logging.Logger = setup_logger(__name__)

# Constants for dictionary keys
RESOURCE_GROUP_L0_KEY: Final[str] = "resource_group_l0"
DATA_LAKE_L1_KEY: Final[str] = "data_lake_l1_key"


@dataclass
class MedallionDataLakeL2Config(ConstructConfigABC):
    """
    A configuration class for TerraformBackendL0.

    Attributes:
        resource_group_l0_config (ResourceGroupL0Config): The configuration for the resource group.
        data_lake_l1_config (DataLakeL1Config): The configuration for the storage account.
    """

    resource_group_l0_config: ResourceGroupL0Config
    data_lake_l1_config: DataLakeL1Config

    @classmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Create a MedallionDataLakeL2Config by unpacking parameters from a configuration dictionary.

        Args:
            dict_ (dict): A dictionary containing the configuration.

        Returns:
            MedallionDataLakeL2Config: A fully-initialized MedallionDataLakeL2Config.
        """
        resource_group_l0_config = ResourceGroupL0Config.from_dict(dict_[RESOURCE_GROUP_L0_KEY])
        data_lake_l1_config = DataLakeL1Config.from_dict(dict_[DATA_LAKE_L1_KEY])

        return cls(resource_group_l0_config=resource_group_l0_config, data_lake_l1_config=data_lake_l1_config)


class MedallionDataLakeL2(Construct, metaclass=CombinedMeta):
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
        config: MedallionDataLakeL2Config,
    ) -> None:
        """
        Initializes the TerraformBackendL0 construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            config (MedallionDataLakeL2Config): The configuration for the Terraform backend.
        """
        super().__init__(scope, id_)

        # Create the resource group
        self.resource_group_l0 = ResourceGroupL0(
            self,
            "ResourceGroupL0",
            env=env,
            config=config.resource_group_l0_config,
        )

        # Create the storage account
        self.storage_account_l0 = DataLakeL1(
            self,
            "StorageAccountL0",
            env=env,
            config=config.data_lake_l1_config,
            resource_group_name=self.resource_group_l0.resource_group.name,
        )
