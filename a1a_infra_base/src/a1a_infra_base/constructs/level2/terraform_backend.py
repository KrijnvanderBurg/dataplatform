"""
Module terraform_backend

This module defines the TerraformBackendStack class, which initializes the Terraform stack
with a local backend, an Azure provider, and creates a resource group and a locked storage account.

Classes:
    TerraformBackendStack: A Terraform stack that sets up the local backend, Azure provider,
                           and creates a resource group and a locked storage account.
"""

from typing import Final

from cdktf import LocalBackend, TerraformStack
from cdktf_cdktf_provider_azurerm.provider import AzurermProvider
from constructs import Construct

from a1a_infra_base.backend import BackendConfig
from a1a_infra_base.constructs.level0.resource_group import ResourceGroupL0
from a1a_infra_base.constructs.level1.storage_account_locked import StorageAccountLockedL1

# Constants for dictionary keys
TERRAFORM_BACKEND_KEY: Final[str] = "terraform_backend"
BACKEND_KEY: Final[str] = "backend"
RESOURCE_GROUP_KEY: Final[str] = "resource_group"
STORAGE_ACCOUNT_KEY: Final[str] = "storage_account"
ENV_KEY: Final[str] = "env"


class TerraformBackendStack(TerraformStack):
    """
    A Terraform stack that sets up the local backend, Azure provider, and creates a resource group
    and a locked storage account based on a given configuration dictionary.

    Example of a minimal config dictionary for this class:
    {
        "env": "prod",
        "terraform_backend": {
            "backend": {
                "path": "init.tfstate"
            },
            "resource_group": {
                "name": "init",
                "location": "GERMANY_WEST_CENTRAL",
                "sequence_number": "01"
            },
            "storage_account": {
                "name": "init",
                "location": "GERMANY_WEST_CENTRAL",
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
                    "delete_retention_days": 7
                }
            },
            "management_lock": {
                "lock_level": "CanNotDelete"
            }
        }
    }
    """

    def __init__(
        self,
        scope: Construct,
        id_: str,
        backend_path: str,
        resource_group: ResourceGroupL0,
        storage_account: StorageAccountLockedL1,
    ) -> None:
        """
        Initializes the TerraformBackendStack using the supplied config dictionary.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            backend_path (str): The path for the local backend.
            resource_group (ResourceGroupL0): The resource group level 0 construct.
            storage_account (StorageAccountLockedL1): The storage account locked level 1 construct.
        """
        super().__init__(scope, id_)

        LocalBackend(self, path=backend_path)

        self._azure_provider = AzurermProvider(
            self,
            "AzureResourceManagerProvider",
            storage_use_azuread=True,
            features=[{}],
        )

        self.resource_group = resource_group
        self.storage_account = storage_account

    @classmethod
    def from_config(cls, scope: Construct, id_: str, config: dict) -> "TerraformBackendStack":
        """
        Create a TerraformBackendStack from a configuration dictionary.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            config (dict): A configuration dictionary. Must include keys:
                - env (string)
                - terraform_backend
                    - backend (dictionary with key 'path')
                    - resource_group (dictionary with RG details)
                    - storage_account (dictionary with SA details)

        Returns:
            TerraformBackendStack: A fully-initialized TerraformBackendStack.
        """
        env = config[ENV_KEY]
        terraform_backend = config[TERRAFORM_BACKEND_KEY]

        backend_cfg = terraform_backend[BACKEND_KEY]
        resource_group_cfg = terraform_backend[RESOURCE_GROUP_KEY]
        storage_account_cfg = terraform_backend[STORAGE_ACCOUNT_KEY]

        backend = BackendConfig.from_config(config=backend_cfg)
        resource_group = ResourceGroupL0.from_config(
            scope=scope, id_="ResourceGroupConstruct", config=resource_group_cfg, env=env
        )
        storage_account = StorageAccountLockedL1.from_config(
            scope=scope,
            id_="StorageAccountConstruct",
            config=storage_account_cfg,
            env=env,
            resource_group_l0=resource_group,
        )

        return cls(
            scope=scope,
            id_=id_,
            backend_path=backend.path,
            resource_group=resource_group,
            storage_account=storage_account,
        )
