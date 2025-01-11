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

from a1a_infra_base.constructs.level1.resource_group_locked import ResourceGroupLockedL1Config
from a1a_infra_base.constructs.level2.storage_account_with_containers import (
    StorageAccountWithContainersL2Config,
)
from a1a_infra_base.constructs.level3.terraform_backend import TerraformBackendL3, TerraformBackendL3Config


@pytest.fixture(name="terraform_backend_l3_config__dict")
def fixture__terraform_backend_l3_config__dict(
    resource_group_locked_l1_config__dict: dict[str, Any],
    storage_account_with_containers_l2_config__dict: dict[str, Any],
) -> dict[str, Any]:
    """
    Fixture that provides a configuration dictionary for TerraformBackendL3Config.

    Returns:
        dict[str, Any]: A configuration dictionary.
    """
    return {
        "resource_group_locked_l1": resource_group_locked_l1_config__dict,
        "storage_account_with_containers_l2": storage_account_with_containers_l2_config__dict,
    }


class TestTerraformBackendL3Config:
    """
    Test suite for the TerraformBackendL1Config class.
    """

    def test__terraform_backend_config__from_dict(self, terraform_backend_l3_config__dict: dict[str, Any]) -> None:
        """
        Test the from_dict method of the TerraformBackendL1Config class.

        Args:
            terraform_backend_l3_config__dict (dict[str, Any]): The terraform backend configuration dictionary.
        """
        config = TerraformBackendL3Config.from_dict(terraform_backend_l3_config__dict)
        assert isinstance(config.resource_group_locked_l1, ResourceGroupLockedL1Config)
        assert isinstance(config.storage_account_with_containers_l2, StorageAccountWithContainersL2Config)


@pytest.fixture(name="terraform_backend_l3_config__instance")
def fixture__terraform_backend_l3_config__instance(
    resource_group_locked_l1_config__instance: ResourceGroupLockedL1Config,
    storage_account_with_containers_l2_config__instance: StorageAccountWithContainersL2Config,
) -> TerraformBackendL3Config:
    """
    Fixture that provides a default configuration for TerraformBackendL1.

    Returns:
        TerraformBackendL1Config: A default configuration instance.
    """
    return TerraformBackendL3Config(
        resource_group_locked_l1=resource_group_locked_l1_config__instance,
        storage_account_with_containers_l2=storage_account_with_containers_l2_config__instance,
    )


class TestTerraformBackendL3:
    """
    Test suite for the TerraformBackendL1 construct.
    """

    def test__terraform_backend__creation(
        self, terraform_backend_l3_config__instance: TerraformBackendL3Config
    ) -> None:
        """
        Test that a TerraformBackendL1 construct creates a resource group and a storage account.

        Args:
            terraform_backend_l3_config__instance (TerraformBackendL1Config): The configuration for the
                Terraform backend.
        """
        app = App()
        stack = TerraformStack(app, "test-stack")
        TerraformBackendL3(stack, "test", env="dev", config=terraform_backend_l3_config__instance)
        synthesized = Testing.synth(stack)

        # resource group
        assert Testing.to_have_resource(
            received=synthesized,
            resource_type=ResourceGroup.TF_RESOURCE_TYPE,
        )

        # management lock
        # note there should be 2 management locks but cant test for that
        assert Testing.to_have_resource(
            received=synthesized,
            resource_type=ManagementLock.TF_RESOURCE_TYPE,
        )

        # storage account
        assert Testing.to_have_resource(
            received=synthesized,
            resource_type=StorageAccount.TF_RESOURCE_TYPE,
        )

        # storage container
        assert Testing.to_have_resource(
            received=synthesized,
            resource_type=StorageContainer.TF_RESOURCE_TYPE,
        )
        # assert Testing.to_be_valid_terraform(synthesized)
