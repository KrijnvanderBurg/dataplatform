"""
Module terraform_backend

This module defines the TerraformBackendStack class, which initializes the Terraform stack
with a local backend and an Azure provider, and creates a resource group and a locked storage account.

Classes:
    TerraformBackendStack: A Terraform stack that sets up the local backend, Azure provider,
                           and creates a resource group and a locked storage account.
"""

from typing import Final

from cdktf import LocalBackend, TerraformStack
from cdktf_cdktf_provider_azurerm.provider import AzurermProvider
from constructs import Construct

from a1a_infra_base.constructs.level0.resource_group import ResourceGroupL0
from a1a_infra_base.constructs.level1.storage_account_locked import StorageAccountLockedL1

TERRAFORM_BACKEND_KEY: Final[str] = "terraform_backend"
BACKEND_KEY: Final[str] = "backend"
RESOURCE_GROUP_KEY: Final[str] = "resource_group"
STORAGE_ACCOUNT_KEY: Final[str] = "storage_account"


class TerraformBackendStack(TerraformStack):
    """
    A Terraform stack that sets up the local backend, Azure provider, and creates a resource group and a locked storage account.

    Attributes:
        azure_provider (AzurermProvider): The Azure provider for Terraform.
        resource_group (ResourceGroupL0): The resource group level 0 construct.
        storage_account (StorageAccountLockedL1): The storage account locked level 1 construct.
    """

    def __init__(self, scope: Construct, id_: str, config: dict) -> None:
        """
        Initializes the TerraformBackendStack.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id (str): The scoped construct ID.
        """
        super().__init__(scope, id_)

        backend_cfg = config[TERRAFORM_BACKEND_KEY][BACKEND_KEY]
        LocalBackend(self, path=backend_cfg["path"])

        self._azure_provider = AzurermProvider(
            self,
            "AzureResourceManagerProvider",
            storage_use_azuread=True,
            features=[{}],
        )

        resource_group_cfg = config[TERRAFORM_BACKEND_KEY][RESOURCE_GROUP_KEY]
        self.resource_group = ResourceGroupL0(self, "ResourceGroupConstruct", resource_group_cfg)

        storage_account_cfg = config[TERRAFORM_BACKEND_KEY][STORAGE_ACCOUNT_KEY]
        self.storage_account = StorageAccountLockedL1(self, "StorageAccountConstruct", storage_account_cfg)

    @classmethod
    def from_config(cls, scope: Construct, id_: str, config: dict) -> "TerraformBackendStack":
        return cls(scope, id_, config)
