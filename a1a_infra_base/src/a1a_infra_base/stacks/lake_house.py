"""
Module data_lake

This module defines the DataLakeStack class, which creates a data lake with multiple storage accounts.
"""

import logging
from dataclasses import dataclass
from typing import Any, Self

from cdktf import LocalBackend, TerraformStack
from cdktf_cdktf_provider_azurerm.provider import AzurermProvider

from a1a_infra_base.constants import AzureLocation
from a1a_infra_base.constructs.level0.management_lock import ManagementLockL0, ManagementLockL0Config
from a1a_infra_base.constructs.level0.resource_group import ResourceGroupL0, ResourceGroupL0Config

# from a1a_infra_base.constructs.level0.storage_account import StorageAccountL0, StorageAccountL0Config
from a1a_infra_base.constructs.level2.data_lake import DATA_LAKE_KEY, DataLakeL2, DataLakeL2Config
from a1a_infra_base.logger import setup_logger
from a1a_infra_base.stacks.ABC import (
    AZURERM_KEY,
    BACKEND_KEY,
    CONSTRUCTS_KEY,
    LOCAL_KEY,
    PROVIDER_KEY,
    CombinedMeta,
    StackABC,
    StackConfigABC,
)
from a1a_infra_base.terraform_backend import TerraformBackendLocalConfig
from a1a_infra_base.terraform_provider import TerraformProviderAzurermConfig
from constructs import Construct

logger: logging.Logger = setup_logger(__name__)


@dataclass
class LakeHouseStackConstructsConfig:
    """TODO"""

    rg_storage: ResourceGroupL0Config
    rg_storage_lock: ManagementLockL0Config
    data_lake: DataLakeL2Config

    @classmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Creates a DataLakeStackConfig instance from a dictionary.

        Args:
            dict_ (dict[str, Any]): The dictionary containing the configuration.

        Returns:
            LakeHouseStackConstructsConfig: A new instance of LakeHouseStackConstructsConfig.
        """
        rg_storage: ResourceGroupL0Config = ResourceGroupL0Config(
            name="storage", location=AzureLocation.GERMANY_WEST_CENTRAL, sequence_number="01"
        )
        rg_storage_lock: ManagementLockL0Config = ManagementLockL0Config(lock_level="CanNotDelete")

        return cls(
            rg_storage=rg_storage,
            rg_storage_lock=rg_storage_lock,
            data_lake=DataLakeL2Config.from_dict(dict_[DATA_LAKE_KEY]),
        )


@dataclass
class LakeHouseStackConfig(StackConfigABC):
    """
    Configuration class for DataLakeStack.

    Attributes:
        backend_local_config (TerraformBackendLocalConfig): Configuration for the local Terraform backend.
        provider_azurerm_config (TerraformProviderAzurermConfig): Configuration for the Azure provider.
        constructs_config (LakeHouseStackConstructsConfig): Configuration for the lake house constructs.
    """

    backend_local_config: TerraformBackendLocalConfig
    provider_azurerm_config: TerraformProviderAzurermConfig
    constructs_config: LakeHouseStackConstructsConfig

    @classmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Creates a DataLakeStackConfig instance from a dictionary.

        Args:
            dict_ (dict[str, Any]): The dictionary containing the configuration.

        Returns:
            DataLakeStackConfig: A new instance of DataLakeStackConfig.
        """
        return cls(
            backend_local_config=TerraformBackendLocalConfig.from_dict(dict_[BACKEND_KEY][LOCAL_KEY]),
            provider_azurerm_config=TerraformProviderAzurermConfig.from_dict(dict_[PROVIDER_KEY][AZURERM_KEY]),
            constructs_config=LakeHouseStackConstructsConfig.from_dict(dict_[CONSTRUCTS_KEY]),
        )


class LakeHouseStack(TerraformStack, StackABC, metaclass=CombinedMeta):
    """
    A Terraform stack that creates a data lake following the medallion architecture pattern.
    Creates a resource group containing four storage accounts:
    - Source storage for raw data
    - Bronze storage for processed data
    - Silver storage for curated data
    - Gold storage for aggregated data

    Each storage account is configured with data lake features (HNS enabled) and appropriate containers.
    The resource group is protected with a CanNotDelete lock.

    Attributes:
        resource_group (ResourceGroupL0): The resource group.
        management_lock (ManagementLockL0): The management lock.
        data_lake_l1 (DataLakeL1): The data lake construct that manages the storage accounts.
    """

    def __init__(
        self,
        scope: Construct,
        id_: str = "LakeHouseStack",
        *,
        env: str,
        config: LakeHouseStackConfig,
    ) -> None:
        """
        Initializes the DataLakeStack construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            config (DataLakeStackConfig): The configuration for the data lake stack.
        """
        super().__init__(scope, id_)

        # Set up the local backend
        LocalBackend(self, path=config.backend_local_config.path)

        # Set up the Azure provider
        AzurermProvider(
            self,
            "AzureRM",
            features=[{}],
            tenant_id=config.provider_azurerm_config.tenant_id,
            subscription_id=config.provider_azurerm_config.subscription_id,
            client_id=config.provider_azurerm_config.client_id,
            client_secret=config.provider_azurerm_config.client_secret,
        )

        # Create the resource group
        self._resource_group = ResourceGroupL0(
            self,
            "ResourceGroupL0",
            env=env,
            config=config.constructs_config.rg_storage,
        )

        # Create the management lock for the resource group
        self._management_lock = ManagementLockL0(
            self,
            "ManagementLockL0",
            _=env,
            config=config.constructs_config.rg_storage_lock,
            resource_id=self._resource_group.resource_group.id,
            resource_name=config.constructs_config.rg_storage.name,
        )

        # Create the data lake storage accounts
        self._data_lake = DataLakeL2(
            self,
            "DataLakeL2",
            env=env,
            config=config.constructs_config.data_lake,
            resource_group_name=self._resource_group.resource_group.name,
        )

    @property
    def resource_group(self) -> ResourceGroupL0:
        """Gets the resource group."""
        return self._resource_group

    @property
    def management_lock(self) -> ManagementLockL0:
        """Gets the management lock."""
        return self._management_lock

    @property
    def data_lake(self) -> DataLakeL2:
        """Gets the data lake construct."""
        return self._data_lake
