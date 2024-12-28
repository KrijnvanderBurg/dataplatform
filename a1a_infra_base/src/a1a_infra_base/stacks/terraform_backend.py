"""
Module terraform_backend

This module defines the TerraformBackendStack class, which initializes the Terraform stack
with a local backend, an Azure provider, and creates a resource group and a locked storage account.

Classes:
    TerraformBackendStack: A Terraform stack that sets up the local backend, Azure provider,
                           and creates a resource group and a locked storage account.
    TerraformBackendStackConfig: A configuration class for TerraformBackendStack.

Example of a config dictionary for this stack:
{
    "env": "dev",
    "terraform_backend": {
        "enabled": true,
        "backend": {
            "type": "local",
            "path": "init.tfstate"
        },
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
            "management_lock": {
                "lock_level": "CanNotDelete",
                "notes": "Necessary for Terraform deployments"
            }
        }
    }
}
"""

from dataclasses import dataclass
from typing import Any, Final, Self

from cdktf import LocalBackend, TerraformStack
from cdktf_cdktf_provider_azurerm.provider import AzurermProvider
from constructs import Construct

from a1a_infra_base.constructs.level0.resource_group import ResourceGroupL0, ResourceGroupL0Config
from a1a_infra_base.constructs.level1.storage_account_locked import StorageAccountLockedL1, StorageAccountLockedL1Config

# Constants for dictionary keys
BACKEND_KEY: Final[str] = "backend"
RESOURCE_GROUP_KEY: Final[str] = "resource_group"
STORAGE_ACCOUNT_KEY: Final[str] = "storage_account"


@dataclass
class TerraformBackendStackConfig:
    """
    A configuration class for TerraformBackendStack.

    This class is responsible for unpacking parameters from a configuration dictionary.
    """

    env: str
    backend_path: str
    resource_group_config: ResourceGroupL0Config
    storage_account_config: StorageAccountLockedL1Config

    @classmethod
    def from_config(cls, env: str, config: dict[str, Any]) -> Self:
        """
        Create a TerraformBackendStackConfig by unpacking parameters from a configuration dictionary.

        Args:
            env (str): The environment name.
            config (dict): A dictionary containing the stack configuration.

        Returns:
            TerraformBackendStackConfig: An instance of TerraformBackendStackConfig.
        """
        backend_cfg = config[BACKEND_KEY]
        resource_group_cfg = config[RESOURCE_GROUP_KEY]
        storage_account_cfg = config[STORAGE_ACCOUNT_KEY]

        backend_path = backend_cfg["path"]
        resource_group_config = ResourceGroupL0Config.from_config(env=env, config=resource_group_cfg)
        storage_account_config = StorageAccountLockedL1Config.from_config(env=env, config=storage_account_cfg)

        return cls(
            env=env,
            backend_path=backend_path,
            resource_group_config=resource_group_config,
            storage_account_config=storage_account_config,
        )


class TerraformBackendStack(TerraformStack):
    """
    A Terraform stack that sets up the local backend, Azure provider, and creates a resource group
    and a locked storage account based on a given configuration dictionary.

    Expected format of 'config':
    {
        "env": "<environment name>",
        "terraform_backend": {
            "enabled": <bool>,
            "backend": {
                "type": "<backend type>",
                "path": "<backend path>"
            },
            "resource_group": {
                "name": "<resource group name>",
                "location": "<location>",
                "sequence_number": "<sequence number>"
            },
            "storage_account": {
                "name": "<storage account name>",
                "location": "<location>",
                "sequence_number": "<sequence number>",
                "resource_group_name": "<resource group name>",
                "account_replication_type": "<replication type>",
                "account_kind": "<account kind>",
                "account_tier": "<account tier>",
                "cross_tenant_replication_enabled": <bool>,
                "access_tier": "<access tier>",
                "shared_access_key_enabled": <bool>,
                "public_network_access_enabled": <bool>,
                "is_hns_enabled": <bool>,
                "local_user_enabled": <bool>,
                "infrastructure_encryption_enabled": <bool>,
                "sftp_enabled": <bool>,
                "blob_properties": {
                    "delete_retention_policy": {
                        "delete_retention_days": <int>
                    }
                },
                "management_lock": {
                    "lock_level": "<lock level>",
                    "notes": "<notes>"
                }
            }
        }
    }
    """

    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        config: TerraformBackendStackConfig,
    ) -> None:
        """
        Initializes the TerraformBackendStack using the supplied config dictionary.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            config (TerraformBackendStackConfig): The configuration for the stack.
        """
        super().__init__(scope, id_)

        LocalBackend(self, path=config.backend_path)

        self._azure_provider = AzurermProvider(
            self,
            "AzureResourceManagerProvider",
            storage_use_azuread=True,
            features=[{}],
        )

        self.resource_group = ResourceGroupL0(
            self,
            "ResourceGroupL0",
            config=config.resource_group_config,
        )
        self.storage_account = StorageAccountLockedL1(
            self,
            "StorageAccountLockedL1",
            config=config.storage_account_config,
            resource_group_l0=self.resource_group,
        )
