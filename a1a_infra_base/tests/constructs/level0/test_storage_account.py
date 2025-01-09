"""
Module for testing the StorageAccountL0 and StorageAccountL0Config classes.

This module contains unit tests for the StorageAccountL0 construct, which is used to create
Azure storage accounts, and the StorageAccountL0Config class, which is used to configure
the StorageAccountL0 construct.


Tests:
    - TestStorageAccountL0Config:
        - test__storage_account_config__from_dict: Tests the from_dict method of the StorageAccountL0Config class.
    - TestBlobPropertiesL0Config:
        - test__blob_properties__from_dict: Tests the from_dict method of the BlobProperties class.
    - TestDeleteRetentionPolicyL0Config:
        - test__delete_retention_policy__from_dict: Tests the from_dict method of the DeleteRetentionPolicy class.
    - TestStorageAccountL0:
        - test__storage_account__creation_with_lock: Tests that a StorageAccountL0 construct creates a storage account
            with a management lock.
        - test__storage_account__creation_without_lock: Tests that a StorageAccountL0 construct creates a storage
            account without a management lock.
"""

from typing import Any

import pytest
from cdktf import App, TerraformStack, Testing
from cdktf_cdktf_provider_azurerm.management_lock import ManagementLock
from cdktf_cdktf_provider_azurerm.storage_account import StorageAccount
from cdktf_cdktf_provider_azurerm.storage_container import StorageContainer

from a1a_infra_base.constants import AzureLocation
from a1a_infra_base.constructs.level0.management_lock import ManagementLockL0Config
from a1a_infra_base.constructs.level0.storage_account import (
    BlobPropertiesL0Config,
    DeleteRetentionPolicyL0Config,
    StorageAccountL0,
    StorageAccountL0Config,
)
from a1a_infra_base.constructs.level0.storage_container import StorageContainerL0Config


class TestBlobPropertiesL0Config:
    """
    Test suite for the BlobProperties class.
    """

    @pytest.fixture
    def dict_(self) -> dict[str, Any]:
        """
        Fixture that provides a configuration dictionary for BlobProperties.

        Returns:
            dict[str, Any]: A configuration dictionary.
        """
        return {"delete_retention_policy_l0": {"days": 7}}

    def test__blob_properties__from_dict(self, dict_: dict[str, Any]) -> None:
        """
        Test the from_dict method of the BlobProperties class.

        Args:
            dict_ (dict[str, Any]): The configuration dictionary.
        """
        blob_properties = BlobPropertiesL0Config.from_dict(dict_)
        assert blob_properties.delete_retention_policy_l0 is not None
        assert blob_properties.delete_retention_policy_l0.days == 7


class TestDeleteRetentionPolicyL0Config:
    """
    Test suite for the DeleteRetentionPolicy class.
    """

    @pytest.fixture
    def dict_(self) -> dict[str, Any]:
        """
        Fixture that provides a configuration dictionary for DeleteRetentionPolicy.

        Returns:
            dict[str, Any]: A configuration dictionary.
        """
        return {"days": 7}

    def test__delete_retention_policy__from_dict(self, dict_: dict[str, Any]) -> None:
        """
        Test the from_dict method of the DeleteRetentionPolicy class.

        Args:
            dict_ (dict[str, Any]): The configuration dictionary.
        """
        delete_retention_policy = DeleteRetentionPolicyL0Config.from_dict(dict_)
        assert delete_retention_policy.days == 7


class TestStorageAccountL0Config:
    """
    Test suite for the StorageAccountL0Config class.
    """

    @pytest.fixture()
    def dict_(self) -> dict[str, Any]:
        """
        Fixture that provides a configuration dictionary for StorageAccountL0Config.

        Returns:
            dict[str, Any]: A configuration dictionary.
        """
        return {
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
            "storage_containers_l0": [{"name": "test_container"}],
            "management_lock_l0": {"lock_level": "CanNotDelete"},
        }

    def test__storage_account_config__from_dict(self, dict_: dict[str, Any]) -> None:
        """
        Test the from_dict method of the StorageAccountL0Config class.

        Args:
            dict_ (dict[str, Any]): The configuration dictionary.
        """
        config = StorageAccountL0Config.from_dict(dict_)
        assert config.name == "init"
        assert config.location == AzureLocation.GERMANY_WEST_CENTRAL
        assert config.sequence_number == "01"
        assert config.account_replication_type == "LRS"
        assert config.account_kind == "StorageV2"
        assert config.account_tier == "Standard"
        assert config.cross_tenant_replication_enabled is False
        assert config.access_tier == "Hot"
        assert config.shared_access_key_enabled is False
        assert config.public_network_access_enabled is True
        assert config.is_hns_enabled is False
        assert config.local_user_enabled is False
        assert config.infrastructure_encryption_enabled is True
        assert config.sftp_enabled is False
        assert config.blob_properties_l0 is not None
        assert config.blob_properties_l0.delete_retention_policy_l0 is not None
        assert config.blob_properties_l0.delete_retention_policy_l0.days == 7
        assert config.storage_containers_l0 is not None
        assert len(config.storage_containers_l0) == 1
        assert config.storage_containers_l0[0].name == "test_container"  # type: ignore
        assert config.management_lock_l0 is not None
        assert config.management_lock_l0.lock_level == "CanNotDelete"


class TestStorageAccountL0:
    """
    Test suite for the StorageAccountL0 construct.
    """

    @pytest.fixture()
    def config(self) -> StorageAccountL0Config:
        """
        Fixture that provides a default configuration for StorageAccountL0.

        Returns:
            StorageAccountL0Config: A default configuration instance.
        """
        return StorageAccountL0Config(
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
            blob_properties_l0=BlobPropertiesL0Config(delete_retention_policy_l0=DeleteRetentionPolicyL0Config(days=7)),
            storage_containers_l0=[StorageContainerL0Config(name="test_container")],
            management_lock_l0=ManagementLockL0Config(
                lock_level="CanNotDelete", notes="Required for Terraform deployments."
            ),
        )

    def test__storage_account__creation_with_lock(self, config: StorageAccountL0Config) -> None:
        """
        Test that a StorageAccountL0 construct creates a storage account with a management lock.

        Args:
            config (StorageAccountL0Config): The configuration for the storage account with a management lock.
        """
        app = App()
        stack = TerraformStack(app, "test-stack")
        StorageAccountL0(stack, "test-account", env="dev", config=config, resource_group_name="test")
        synthesized = Testing.synth(stack)
        assert Testing.to_have_resource_with_properties(
            received=synthesized,
            resource_type=StorageAccount.TF_RESOURCE_TYPE,
            properties={
                "name": "sainitdevgwc01",
                "location": "germany west central",
                "resource_group_name": "test",
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

    def test__storage_account__creation_without_lock(self, config: StorageAccountL0Config) -> None:
        """
        Test that a StorageAccountL0 construct creates a storage account without a management lock.

        Args:
            config (StorageAccountL0Config): The configuration for the storage account without a management lock.
        """
        config.management_lock_l0 = None
        app = App()
        stack = TerraformStack(app, "test-stack")
        StorageAccountL0(stack, "test-account", env="dev", config=config, resource_group_name="test")
        synthesized = Testing.synth(stack)
        assert Testing.to_have_resource_with_properties(
            received=synthesized,
            resource_type=StorageAccount.TF_RESOURCE_TYPE,
            properties={
                "name": "sainitdevgwc01",
                "location": "germany west central",
                "resource_group_name": "test",
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

        assert not Testing.to_have_resource(
            received=synthesized,
            resource_type=ManagementLock.TF_RESOURCE_TYPE,
        )

        # assert Testing.to_be_valid_terraform(synthesized)
