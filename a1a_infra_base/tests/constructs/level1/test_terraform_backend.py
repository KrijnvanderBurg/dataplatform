"""
Module for testing the TerraformBackendL1 and TerraformBackendL1Config classes.

This module contains unit tests for the TerraformBackendL1 construct, which is used to create
a Terraform backend, and the TerraformBackendL1Config class, which is used to configure
the TerraformBackendL1 construct.

Fixtures:
    - TestTerraformBackendL1Config:
        - dict_: Provides a configuration dictionary for TerraformBackendL1Config.
    - TestTerraformBackendL1:
        - config: Provides a default configuration for TerraformBackendL1.
        - stack: Provides a TerraformStack instance.

Tests:
    - TestTerraformBackendL1Config:
        - test__terraform_backend_config__from_dict: Tests the from_dict method of the TerraformBackendL1Config class.
    - TestTerraformBackendL1:
        - test__terraform_backend__creation: Tests that a TerraformBackendL1 construct creates a resource group
          and a storage account.
"""

import pytest
from cdktf import App, TerraformStack, Testing
from cdktf_cdktf_provider_azurerm.resource_group import ResourceGroup
from cdktf_cdktf_provider_azurerm.storage_account import StorageAccount

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

    @pytest.fixture
    def dict_(self) -> dict:
        """
        Fixture that provides a configuration dictionary for TerraformBackendL1Config.

        Returns:
            dict: A configuration dictionary.
        """
        return {
            "resource_group_l0": {
                "name": "init",
                "location": "germany west central",
                "sequence_number": "01",
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
                "blob_properties": {"delete_retention_policy": {"delete_retention_days": 7}},
                "containers": [{"name": "terraform"}],
                "management_lock": {"lock_level": "CanNotDelete", "notes": "Required for Terraform deployments."},
            },
        }

    def test__terraform_backend_config__from_dict(self, dict_: dict) -> None:
        """
        Test the from_dict method of the TerraformBackendL1Config class.

        Args:
            dict_ (dict): The configuration dictionary.
        """
        config = TerraformBackendL1Config.from_dict(dict_)
        assert config.resource_group_config.name == "init"
        assert config.resource_group_config.location == AzureLocation.GERMANY_WEST_CENTRAL
        assert config.resource_group_config.sequence_number == "01"
        assert config.storage_account_config.name == "init"
        assert config.storage_account_config.location == AzureLocation.GERMANY_WEST_CENTRAL
        assert config.storage_account_config.sequence_number == "01"
        assert config.storage_account_config.account_replication_type == "LRS"
        assert config.storage_account_config.account_kind == "StorageV2"
        assert config.storage_account_config.account_tier == "Standard"
        assert config.storage_account_config.cross_tenant_replication_enabled is False
        assert config.storage_account_config.access_tier == "Hot"
        assert config.storage_account_config.shared_access_key_enabled is False
        assert config.storage_account_config.public_network_access_enabled is True
        assert config.storage_account_config.is_hns_enabled is False
        assert config.storage_account_config.local_user_enabled is False
        assert config.storage_account_config.infrastructure_encryption_enabled is True
        assert config.storage_account_config.sftp_enabled is False
        assert config.storage_account_config.blob_properties.delete_retention_policy.days == 7
        assert len(config.storage_account_config.containers) == 1
        assert config.storage_account_config.containers[0].name == "terraform"
        assert config.storage_account_config.management_lock is not None
        assert config.storage_account_config.management_lock.lock_level == "CanNotDelete"
        assert config.storage_account_config.management_lock.notes == "Required for Terraform deployments."


class TestTerraformBackendL1:
    """
    Test suite for the TerraformBackendL1 construct.
    """

    @pytest.fixture
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
                blob_properties=BlobPropertiesL0Config(delete_retention_policy=DeleteRetentionPolicyL0Config(days=7)),
                containers=[StorageContainerL0Config(name="terraform")],
                management_lock=ManagementLockL0Config(
                    lock_level="CanNotDelete", notes="Required for Terraform deployments."
                ),
            ),
        )

    @pytest.fixture
    def stack(self) -> TerraformStack:
        """
        Fixture that provides a TerraformStack instance.

        Returns:
            TerraformStack: A TerraformStack instance.
        """
        app = App()
        return TerraformStack(app, "test-stack")

    def test__terraform_backend__creation(self, stack: TerraformStack, config: TerraformBackendL1Config) -> None:
        """
        Test that a TerraformBackendL1 construct creates a resource group and a storage account.

        Args:
            stack (TerraformStack): The Terraform stack.
            config (TerraformBackendL1Config): The configuration for the Terraform backend.
        """
        TerraformBackendL1(stack, "test-backend", env="dev", config=config)
        synthesized = Testing.synth(stack)
        assert Testing.to_have_resource_with_properties(
            received=synthesized,
            resource_type=ResourceGroup.TF_RESOURCE_TYPE,
            properties={
                "name": "rg-init-dev-germanywestcentral-01",
                "location": "Germany West Central",
            },
        )
        assert Testing.to_have_resource_with_properties(
            received=synthesized,
            resource_type=StorageAccount.TF_RESOURCE_TYPE,
            properties={
                "name": "stgdevinitgermanywestcentral01",
                "location": "Germany West Central",
                "resource_group_name": "rg-init-dev-germanywestcentral-01",
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
