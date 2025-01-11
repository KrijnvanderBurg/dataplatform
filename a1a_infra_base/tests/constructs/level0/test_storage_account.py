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
        - test__storage_account__creation: Tests that a StorageAccountL0 construct creates a storage account
"""

from typing import Any

import pytest
from cdktf import App, TerraformStack, Testing
from cdktf_cdktf_provider_azurerm.storage_account import StorageAccount

from a1a_infra_base.constants import AzureLocation
from a1a_infra_base.constructs.level0.storage_account import (
    BlobPropertiesL0Config,
    DeleteRetentionPolicyL0Config,
    StorageAccountL0,
    StorageAccountL0Config,
)


@pytest.fixture(name="blob_properties_l0_config__dict")
def fixture__blob_properties_l0_config__dict() -> dict[str, Any]:
    """
    Fixture that provides a configuration dictionary for BlobProperties.

    Returns:
        dict[str, Any]: A configuration dictionary.
    """
    return {"delete_retention_policy_l0": {"days": 7}}


class TestBlobPropertiesL0Config:
    """
    Test suite for the BlobProperties class.
    """

    def test__blob_properties__from_dict(self, blob_properties_l0_config__dict: dict[str, Any]) -> None:
        """
        Test the from_dict method of the BlobProperties class.

        Args:
            blob_properties_l0_config__dict (dict[str, Any]): The configuration dictionary fixture.
        """
        blob_properties = BlobPropertiesL0Config.from_dict(blob_properties_l0_config__dict)
        assert blob_properties.delete_retention_policy_l0 is not None
        assert blob_properties.delete_retention_policy_l0.days == 7


@pytest.fixture(name="delete_retention_policy_l0_config__dict")
def fixture__delete_retention_policy_l0_config__dict() -> dict[str, Any]:
    """
    Fixture that provides a configuration dictionary for DeleteRetentionPolicy.

    Returns:
        dict[str, Any]: A configuration dictionary fixture.
    """
    return {"days": 7}


class TestDeleteRetentionPolicyL0Config:
    """
    Test suite for the DeleteRetentionPolicy class.
    """

    def test__delete_retention_policy__from_dict(self, delete_retention_policy_l0_config__dict: dict[str, Any]) -> None:
        """
        Test the from_dict method of the DeleteRetentionPolicy class.

        Args:
            delete_retention_policy_l0_config__dict (dict[str, Any]): The configuration dictionary.
        """
        delete_retention_policy = DeleteRetentionPolicyL0Config.from_dict(delete_retention_policy_l0_config__dict)
        assert delete_retention_policy.days == 7


@pytest.fixture(name="storage_account_l0_config__dict")
def fixture__storage_account_l0_config__dict() -> dict[str, Any]:
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
    }


class TestStorageAccountL0Config:
    """
    Test suite for the StorageAccountL0Config class.
    """

    def test__storage_account_config__from_dict(self, storage_account_l0_config__dict: dict[str, Any]) -> None:
        """
        Test the from_dict method of the StorageAccountL0Config class.

        Args:
            storage_account_l0_config__dict (dict[str, Any]): The configuration dictionary fixture.
        """
        config = StorageAccountL0Config.from_dict(storage_account_l0_config__dict)
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


@pytest.fixture(name="storage_account_l0_config__instance")
def fixture__storage_account_l0_config__instance() -> StorageAccountL0Config:
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
    )


class TestStorageAccountL0:
    """
    Test suite for the StorageAccountL0 construct.
    """

    def test__storage_account__creation(self, storage_account_l0_config__instance: StorageAccountL0Config) -> None:
        """
        Test that a StorageAccountL0 construct creates a storage account without a management lock.

        Args:
            storage_account_l0_config__instance (StorageAccountL0Config): The fixture configuration for the storage account without a management lock.
        """
        app = App()
        stack = TerraformStack(app, "test-stack")
        StorageAccountL0(
            stack, "test-account", env="dev", config=storage_account_l0_config__instance, resource_group_name="test"
        )
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

        # assert Testing.to_be_valid_terraform(synthesized)
