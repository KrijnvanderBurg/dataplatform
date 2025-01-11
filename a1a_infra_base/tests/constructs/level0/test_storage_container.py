"""
Module for testing the StorageContainerL0 and StorageContainerL0Config classes.

This module contains unit tests for the StorageContainerL0 construct, which is used to create
Azure storage containers, and the StorageContainerL0Config class, which is used to configure
the StorageContainerL0 construct.


Tests:
    - TestStorageContainerL0Config:
        - test__storage_container_config__from_dict: Tests the from_dict method of the StorageContainerL0Config class.
    - TestStorageContainerL0:
        - test__storage_container__creation: Tests that a StorageContainerL0 construct creates a storage container.
"""

from typing import Any

import pytest
from cdktf import App, TerraformStack, Testing
from cdktf_cdktf_provider_azurerm.storage_container import StorageContainer

from a1a_infra_base.constructs.level0.storage_container import StorageContainerL0, StorageContainerL0Config


@pytest.fixture(name="storage_container_l0_config__dict")
def fixture__storage_container_l0_config__dict() -> dict[str, Any]:
    """
    Fixture that provides a configuration dictionary for StorageContainerL0Config.

    Returns:
        dict[str, Any]: A configuration dictionary.
    """
    return {
        "name": "test-container",
    }


class TestStorageContainerL0Config:
    """
    Test suite for the StorageContainerL0Config class.
    """

    def test__storage_container_config__from_dict(self, storage_container_l0_config__dict: dict[str, Any]) -> None:
        """
        Test the from_dict method of the StorageContainerL0Config class.

        Args:
            storage_container_l0_config__dict (dict[str, Any]): The configuration dictionary.
        """
        config = StorageContainerL0Config.from_dict(storage_container_l0_config__dict)
        assert config.name == "test-container"


@pytest.fixture(name="storage_container_l0_config__instance")
def fixture__storage_container_l0_config__instance() -> StorageContainerL0Config:
    """
    Fixture that provides a default configuration for StorageContainerL0.

    Returns:
        StorageContainerL0Config: A default configuration instance.
    """
    return StorageContainerL0Config(
        name="test-container",
    )


class TestStorageContainerL0:
    """
    Test suite for the StorageContainerL0 construct.
    """

    def test__storage_container__creation(
        self, storage_container_l0_config__instance: StorageContainerL0Config
    ) -> None:
        """
        Test that a StorageContainerL0 construct creates a storage container.

        Args:
            storage_container_l0_config__instance (StorageContainerL0Config): The configuration for the storage container.
        """
        app = App()
        stack = TerraformStack(app, "test-stack")
        StorageContainerL0(
            stack,
            "test-container",
            _="dev",
            config=storage_container_l0_config__instance,
            storage_account_id="test-account-id",
        )
        synthesized = Testing.synth(stack)
        assert Testing.to_have_resource_with_properties(
            received=synthesized,
            resource_type=StorageContainer.TF_RESOURCE_TYPE,
            properties={
                "name": "test-container",
                "storage_account_id": "test-account-id",
            },
        )
        # assert Testing.to_be_valid_terraform(synthesized)
