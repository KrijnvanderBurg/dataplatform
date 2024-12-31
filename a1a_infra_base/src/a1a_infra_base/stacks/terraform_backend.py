"""
Module terraform_backend

This module defines the TerraformBackendStack class, which initializes the Terraform stack
with a local backend, an Azure provider, and creates a resource group and a locked storage account.

Classes:
    TerraformBackendStack: A Terraform stack that sets up the local backend, Azure provider,
                           and creates a resource group and a locked storage account.
    TerraformBackendStackConfig: A configuration class for TerraformBackendStack.
"""

import logging
from dataclasses import dataclass
from typing import Any, Final, Self

from cdktf import LocalBackend, TerraformStack
from cdktf_cdktf_provider_azurerm.provider import AzurermProvider
from constructs import Construct

from a1a_infra_base.backend import BackendLocalConfig
from a1a_infra_base.constructs.level0.resource_group import ResourceGroupL0, ResourceGroupL0Config
from a1a_infra_base.constructs.level0.storage_account import StorageAccountL0, StorageAccountL0Config
from a1a_infra_base.logger import setup_logger
from a1a_infra_base.provider import ProviderAzurermConfig
from a1a_infra_base.stacks.stack_abc import StackConfigABC

logger: logging.Logger = setup_logger(__name__)

# Constants for dictionary keys
BACKEND_KEY: Final[str] = "backend"

PROVIDER_KEY: Final[str] = "provider"
AZURERM_KEY: Final[str] = "azurerm"

CONSTRUCTS_KEY: Final[str] = "constructs"
RESOURCE_GROUP_KEY: Final[str] = "resource_group"
STORAGE_ACCOUNT_KEY: Final[str] = "storage_account"


@dataclass
class TerraformBackendStackConfig(StackConfigABC):
    """
    A configuration class for TerraformBackendStack.

    This class is responsible for unpacking parameters from a configuration dictionary.

    Attributes:
        backend_local_config (BackendLocalConfig): The configuration for the Terraform backend.
        provider_azurerm_config (ProviderAzurermConfig): The configuration for the Terraform AzureRM provider.
        resource_group_config (ResourceGroupL0Config): The configuration for the resource group.
        storage_account_config (StorageAccountL0Config): The configuration for the storage account.
    """

    backend_local_config: BackendLocalConfig
    provider_azurerm_config: ProviderAzurermConfig
    resource_group_config: ResourceGroupL0Config
    storage_account_config: StorageAccountL0Config

    @classmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Create a TerraformBackendStackConfig by unpacking parameters from a configuration dictionary.

        Expected format of 'dict_':
        {
            "env": "prod",
            "stacks": [
                {
                    "name": "terraform_backend",
                    "enabled": true,
                    "provider": {
                        "azurerm": {
                            "tenant_id": "00000000-0000-0000-0000-000000000000",
                            "subscription_id": "00000000-0000-0000-0000-000000000000",
                            "client_id": "00000000-0000-0000-0000-000000000000",
                            "client_secret": "00000000-0000-0000-0000-000000000000"
                        }
                    },
                    "backend": {
                        "type": "local",
                        "path": "tfstate/init.tfstate"
                    },
                    "constructs": {
                        "resource_group": {
                            "name": "init",
                            "location": "germany west central",
                            "sequence_number": "01"
                        },
                        "storage_account": {
                            "name": "init",
                            "location": "germany west central",
                            "sequence_number": "01",
                            "resource_group_name": "init",
                            "account_replication_type": "LRS",
                            "account_kind": "StorageV2",
                            "account_tier": "Standard",
                            "cross_tenant_replication_enabled": false,
                            "access_tier": "Hot",
                            "shared_access_key_enabled": false,
                            "public_network_access_enabled": true,
                            "is_hns_enabled": false,
                            "local_user_enabled": false,
                            "infrastructure_encryption_enabled": true,
                            "sftp_enabled": false,
                            "blob_properties": {
                                "delete_retention_policy": {
                                    "delete_retention_days": 7
                                }
                            },
                            "containers": [
                                {
                                    "name": "terraform"
                                }
                            ],
                            "management_lock": {
                                "name": "init",
                                "lock_level": "CanNotDelete",
                                "notes": "Required for Terraform deployments."
                            }
                        }
                    }
                }
            ]
        }

        Args:
            dict_ (dict): A dictionary containing the stack configuration.

        Returns:
            TerraformBackendStackConfig: A fully-initialized TerraformBackendStackConfig.
        """
        backend_local_config = BackendLocalConfig.from_dict(dict_[BACKEND_KEY])
        provider_azurerm_config = ProviderAzurermConfig.from_dict(dict_[PROVIDER_KEY][AZURERM_KEY])

        constructs_config = dict_[CONSTRUCTS_KEY]
        resource_group_config = ResourceGroupL0Config.from_dict(dict_=constructs_config[RESOURCE_GROUP_KEY])
        storage_account_config = StorageAccountL0Config.from_dict(dict_=constructs_config[STORAGE_ACCOUNT_KEY])

        return cls(
            backend_local_config=backend_local_config,
            provider_azurerm_config=provider_azurerm_config,
            resource_group_config=resource_group_config,
            storage_account_config=storage_account_config,
        )


class TerraformBackendStack(TerraformStack):
    """
    A Terraform stack that sets up the local backend, Azure provider, and creates a resource group
    and a locked storage account based on a given configuration dictionary.

    Attributes:
        resource_group_l0 (ResourceGroupL0): The resource group construct.
        storage_account_l0 (StorageAccountL0): The storage account construct.
    """

    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        env: str,
        backend_local_config: BackendLocalConfig,
        provider_azurerm_config: ProviderAzurermConfig,
        resource_group_config: ResourceGroupL0Config,
        storage_account_config: StorageAccountL0Config,
    ) -> None:
        """
        Initializes the TerraformBackendStack construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            backend_local_config (BackendLocalConfig): The configuration for the Terraform backend.
            provider_azurerm_config (ProviderAzurermConfig): The configuration for the Terraform AzureRM provider.
            resource_group_config (ResourceGroupL0Config): The configuration for the resource group.
            storage_account_config (StorageAccountL0Config): The configuration for the storage account.
        """
        super().__init__(scope, id_)

        # Set up the local backend
        LocalBackend(self, path=backend_local_config.path)

        # Set up the Azure provider
        AzurermProvider(
            self,
            "AzureRM",
            features=[{}],
            tenant_id=provider_azurerm_config.tenant_id,
            subscription_id=provider_azurerm_config.subscription_id,
            client_id=provider_azurerm_config.client_id,
            client_secret=provider_azurerm_config.client_secret,
        )

        # Create the resource group
        self.resource_group_l0 = ResourceGroupL0(
            self,
            "ResourceGroupL0",
            env=env,
            name=resource_group_config.name,
            location=resource_group_config.location,
            sequence_number=resource_group_config.sequence_number,
            management_lock=resource_group_config.management_lock,
        )

        # Create the storage account
        self.storage_account_l0 = StorageAccountL0(
            self,
            "StorageAccountL0",
            env=env,
            name=storage_account_config.name,
            location=storage_account_config.location,
            resource_group_name=self.resource_group_l0.resource_group.name,
            sequence_number=storage_account_config.sequence_number,
            account_replication_type=storage_account_config.account_replication_type,
            account_kind=storage_account_config.account_kind,
            account_tier=storage_account_config.account_tier,
            cross_tenant_replication_enabled=storage_account_config.cross_tenant_replication_enabled,
            access_tier=storage_account_config.access_tier,
            shared_access_key_enabled=storage_account_config.shared_access_key_enabled,
            public_network_access_enabled=storage_account_config.public_network_access_enabled,
            is_hns_enabled=storage_account_config.is_hns_enabled,
            local_user_enabled=storage_account_config.local_user_enabled,
            infrastructure_encryption_enabled=storage_account_config.infrastructure_encryption_enabled,
            sftp_enabled=storage_account_config.sftp_enabled,
            blob_properties=storage_account_config.blob_properties,
            containers=storage_account_config.containers,
            management_lock=storage_account_config.management_lock,
        )

    @classmethod
    def from_config(cls, scope: Construct, id_: str, env: str, config: TerraformBackendStackConfig) -> Self:
        """
        Create a TerraformBackendStack instance from a TerraformBackendStackConfig object.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            config (TerraformBackendStackConfig): The configuration object for the Terraform stack.

        Returns:
            TerraformBackendStack: A fully-initialized TerraformBackendStack instance.
        """
        return cls(
            scope,
            id_,
            env=env,
            backend_local_config=config.backend_local_config,
            provider_azurerm_config=config.provider_azurerm_config,
            resource_group_config=config.resource_group_config,
            storage_account_config=config.storage_account_config,
        )
