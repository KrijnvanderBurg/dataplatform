"""
Module for testing the TerraformBackendL1 and TerraformBackendL1Config classes.

This module contains unit tests for the TerraformBackendL1 construct, which is used to create
a Terraform backend, and the TerraformBackendL1Config class, which is used to configure
the TerraformBackendL1 construct.


Tests:
    - TestTerraformBackendL1Config:
        - test__terraform_backend_config__from_dict: Tests the from_dict method of the TerraformBackendL1Config class.
    - TestTerraformBackendL1:
        - test__terraform_backend__creation: Tests that a TerraformBackendL1 construct creates a resource group and a
            storage account.
"""

from typing import Any

import pytest
from cdktf import App, TerraformStack, Testing
from cdktf_cdktf_provider_azurerm.management_lock import ManagementLock
from cdktf_cdktf_provider_azurerm.resource_group import ResourceGroup
from cdktf_cdktf_provider_azurerm.storage_account import StorageAccount
from cdktf_cdktf_provider_azurerm.storage_container import StorageContainer

from a1a_infra_base.constants import AzureLocation
from a1a_infra_base.constructs.level0.management_lock import ManagementLockL0Config
from a1a_infra_base.constructs.level0.resource_group import ResourceGroupL0Config
from a1a_infra_base.constructs.level0.storage_account import (
    BlobPropertiesL0Config,
    DeleteRetentionPolicyL0Config,
    StorageAccountL0Config,
)
from a1a_infra_base.constructs.level0.storage_container import StorageContainerL0Config
from a1a_infra_base.constructs.level1.terraform_backend import TerraformBackendL1, TerraformBackendL1Config


class TestTerraformBackendL1Config:
    """
    Test suite for the TerraformBackendL1Config class.
    """

    @pytest.fixture()
    def dict_(self) -> dict[str, Any]:
        """
        Fixture that provides a configuration dictionary for TerraformBackendL1Config.

        Returns:
            dict[str, Any]: A configuration dictionary.
        """
        return {
            "resource_group_l0": {
                "name": "init",
                "location": "germany west central",
                "sequence_number": "01",
                "management_lock_l0": {
                    "lock_level": "CanNotDelete",
                    "notes": "Required for Terraform deployments.",
                },
            },
            "storage_account_l0": {
                "name": "init",
                "location": "germany west central",
                "sequence_number": "01",
                "account_replication_type": "LRS",
                "account_kind": "StorageV2",
                "account_tier": "Standard",
                "cross_tenant_replication_enabled": False,
                "access_tier": "Hot",
                "shared_access_key_enabled": False,
                "public_network_access_enabled": True,
                "is_hns_enabled": False,
                "local_user_enabled": False,
                "infrastructure_encryption_enabled": True,
                "sftp_enabled": False,
                "blob_properties_l0": {"delete_retention_policy_l0": {"days": 7}},
                "storage_containers_l0": [{"name": "terraform"}],
                "management_lock_l0": {"lock_level": "CanNotDelete", "notes": "Required for Terraform deployments."},
            },
        }

    def test__terraform_backend_config__from_dict(self, dict_: dict[str, Any]) -> None:
        """
        Test the from_dict method of the TerraformBackendL1Config class.

        Args:
            dict_ (dict[str, Any]): The terraform backend configuration dictionary.
        """
        config = TerraformBackendL1Config.from_dict(dict_)
        assert isinstance(config.resource_group_config, ResourceGroupL0Config)
        assert isinstance(config.storage_account_config, StorageAccountL0Config)


class TestTerraformBackendL1:
    """
    Test suite for the TerraformBackendL1 construct.
    """

    @pytest.fixture()
    def config(self) -> TerraformBackendL1Config:
        """
        Fixture that provides a default configuration for TerraformBackendL1.

        Returns:
            TerraformBackendL1Config: A default configuration instance.
        """
        return TerraformBackendL1Config(
            resource_group_config=ResourceGroupL0Config(
                name="init",
                location=AzureLocation.GERMANY_WEST_CENTRAL,
                sequence_number="01",
                management_lock_l0=ManagementLockL0Config(
                    lock_level="CanNotDelete", notes="Required for Terraform deployments."
                ),
            ),
            storage_account_config=StorageAccountL0Config(
                name="init",
                location=AzureLocation.GERMANY_WEST_CENTRAL,
                sequence_number="01",
                account_replication_type="LRS",
                account_kind="StorageV2",
                account_tier="Standard",
                cross_tenant_replication_enabled=False,
                access_tier="Hot",
                shared_access_key_enabled=False,
                public_network_access_enabled=True,
                is_hns_enabled=False,
                local_user_enabled=False,
                infrastructure_encryption_enabled=True,
                sftp_enabled=False,
                blob_properties_l0=BlobPropertiesL0Config(
                    delete_retention_policy_l0=DeleteRetentionPolicyL0Config(days=7)
                ),
                storage_containers_l0=[StorageContainerL0Config(name="test_container")],
                management_lock_l0=ManagementLockL0Config(
                    lock_level="CanNotDelete", notes="Required for Terraform deployments."
                ),
            ),
        )

    def test__terraform_backend__creation(self, config: TerraformBackendL1Config) -> None:
        """
        Test that a TerraformBackendL1 construct creates a resource group and a storage account.

        Args:
            config (TerraformBackendL1Config): The configuration for the Terraform backend.
        """
        app = App()
        stack = TerraformStack(app, "test-stack")
        TerraformBackendL1(stack, "test", env="dev", config=config)
        synthesized = Testing.synth(stack)
        # resource group
        assert Testing.to_have_resource_with_properties(
            received=synthesized,
            resource_type=ResourceGroup.TF_RESOURCE_TYPE,
            properties={
                "name": "rg-init-dev-gwc-01",
                "location": "germany west central",
            },
        )
        assert Testing.to_have_resource_with_properties(
            received=synthesized,
            resource_type=ManagementLock.TF_RESOURCE_TYPE,
            properties={
                "name": "rg-init-dev-gwc-01-lock",
                "lock_level": "CanNotDelete",
                "notes": "Required for Terraform deployments.",
            },
        )
        # storage account
        assert Testing.to_have_resource_with_properties(
            received=synthesized,
            resource_type=StorageAccount.TF_RESOURCE_TYPE,
            properties={
                "name": "sainitdevgwc01",
                "location": "germany west central",
                # "resource_group_name": "", # cannot be tested as its dynamic in terraform hcl
                "account_replication_type": "LRS",
                "account_kind": "StorageV2",
                "account_tier": "Standard",
                "cross_tenant_replication_enabled": False,
                "access_tier": "Hot",
                "shared_access_key_enabled": False,
                "public_network_access_enabled": True,
                "is_hns_enabled": False,
                "local_user_enabled": False,
                "infrastructure_encryption_enabled": True,
                "sftp_enabled": False,
                "blob_properties": {"delete_retention_policy": {"days": 7}},
            },
        )
        assert Testing.to_have_resource_with_properties(
            received=synthesized,
            resource_type=ManagementLock.TF_RESOURCE_TYPE,
            properties={
                "lock_level": "CanNotDelete",
                "name": "sainitdevgwc01-lock",
                "notes": "Required for Terraform deployments.",
            },
        )
        assert Testing.to_have_resource_with_properties(
            received=synthesized,
            resource_type=StorageContainer.TF_RESOURCE_TYPE,
            properties={
                "name": "test_container",
            },
        )
        # assert Testing.to_be_valid_terraform(synthesized)
