"""
Module for testing the StorageAccountL0 and StorageAccountLockedL1Config classes.

This module contains unit tests for the StorageAccountL0 construct, which is used to create
Azure storage accounts, and the StorageAccountLockedL1Config class, which is used to configure
the StorageAccountL0 construct.


Tests:
    - TestStorageAccountLockedL1Config:
        - test__storage_account_config__from_dict: Tests the from_dict method of the StorageAccountLockedL1Config class.
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

from a1a_infra_base.constructs.level0.management_lock import ManagementLockL0Config
from a1a_infra_base.constructs.level0.storage_account import StorageAccountL0Config
from a1a_infra_base.constructs.level1.storage_account_locked import StorageAccountLockedL1, StorageAccountLockedL1Config


@pytest.fixture(name="storage_account_locked_l1_config__dict")
def fixture__storage_account_locked_l1_config__dict(
    storage_account_l0_config__dict: dict[str, Any],
    management_lock_l0_config__dict: dict[str, Any],
) -> dict[str, Any]:
    """
    Fixture that provides a configuration dictionary for StorageAccountLockedL1Config.

    Returns:
        dict[str, Any]: A configuration dictionary.
    """
    return {
        "storage_account_l0": storage_account_l0_config__dict,
        "management_lock_l0": management_lock_l0_config__dict,
    }


class TestStorageAccountLockedL1Config:
    """
    Test suite for the StorageAccountLockedL1Config class.
    """

    def test__storage_account_config__from_dict(self, storage_account_locked_l1_config__dict: dict[str, Any]) -> None:
        """
        Test the from_dict method of the StorageAccountLockedL1Config class.

        Args:
            storage_account_locked_l1_config__dict (dict[str, Any]): The configuration dictionary.
        """
        config = StorageAccountLockedL1Config.from_dict(storage_account_locked_l1_config__dict)
        assert isinstance(config.storage_account_l0, StorageAccountL0Config)
        assert isinstance(config.management_lock_l0, ManagementLockL0Config)


@pytest.fixture(name="storage_account_locked_l1_config__instance")
def fixture__storage_account_locked_l1_config__instance(
    storage_account_l0_config__instance: StorageAccountL0Config,
    management_lock_l0_config__instance: ManagementLockL0Config,
) -> StorageAccountLockedL1Config:
    """
    Fixture that provides a default configuration for StorageAccountL0.

    Returns:
        StorageAccountLockedL1Config: A default configuration instance.
    """
    return StorageAccountLockedL1Config(
        storage_account_l0=storage_account_l0_config__instance,
        management_lock_l0=management_lock_l0_config__instance,
    )


class TestStorageAccountL0:
    """
    Test suite for the StorageAccountL0 construct.
    """

    def test__storage_account__creation_with_lock(
        self, storage_account_locked_l1_config__instance: StorageAccountLockedL1Config
    ) -> None:
        """
        Test that a StorageAccountL0 construct creates a storage account with a management lock.

        Args:
            storage_account_locked_l1_config__instance (StorageAccountLockedL1Config): The configuration for the storage account with a management lock.
        """
        app = App()
        stack = TerraformStack(app, "test-stack")
        StorageAccountLockedL1(
            stack,
            "test-account",
            env="dev",
            config=storage_account_locked_l1_config__instance,
            resource_group_name="test",
        )
        synthesized = Testing.synth(stack)
        assert Testing.to_have_resource(
            received=synthesized,
            resource_type=StorageAccount.TF_RESOURCE_TYPE,
        )

        assert Testing.to_have_resource(
            received=synthesized,
            resource_type=ManagementLock.TF_RESOURCE_TYPE,
        )

        # assert Testing.to_be_valid_terraform(synthesized)
