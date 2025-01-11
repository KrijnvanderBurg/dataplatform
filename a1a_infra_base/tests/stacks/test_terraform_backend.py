"""
Module for testing the TerraformBackendStack and TerraformBackendStackConfig classes.

This module contains unit tests for the TerraformBackendStack class, which initializes the Terraform stack
with a local backend, an Azure provider, and creates a resource group and a locked storage account,
and the TerraformBackendStackConfig class, which is used to configure the TerraformBackendStack.


Tests:
    - test_terraform_backend_stack: Tests that a TerraformBackendStack creates a local backend and an AzureRM provider.
"""

from typing import Any

import pytest
from cdktf import App, Testing
from cdktf_cdktf_provider_azurerm.provider import AzurermProvider
from cdktf_cdktf_provider_azurerm.resource_group import ResourceGroup

from a1a_infra_base.backend import BackendLocalConfig
from a1a_infra_base.constructs.level3.terraform_backend import TerraformBackendL3Config
from a1a_infra_base.provider import ProviderAzurermConfig
from a1a_infra_base.stacks.terraform_backend import TerraformBackendStack, TerraformBackendStackConfig


@pytest.fixture(name="terraform_backend_l3_config__dict")
def fixture__terraform_backend_l3_config__dict(terraform_backend_l3_config__dict: dict[str, Any]) -> dict[str, Any]:
    """
    Fixture that provides a configuration dictionary for TerraformBackendStackConfig.

    Returns:
        dict[str, Any]: A configuration dictionary.
    """
    return {
        "backend": {"path": "test/local/path"},
        "provider": {
            "azurerm": {
                "tenant_id": "test-tenant-id",
                "subscription_id": "test-sub-id",
                "client_id": "test-client-id",
                "client_secret": "test-client-secret",
            }
        },
        "constructs": {"terraform_backend_l3": terraform_backend_l3_config__dict},
    }


class TestTerraformBackendStackConfig:
    """
    Test suite for the TerraformBackendStackConfig class.
    """

    def test__terraform_backend_stack__from_dict(self, terraform_backend_l3_config__dict: dict[str, Any]) -> None:
        """
        Test the from_dict method of the TerraformBackendStackConfig class.

        Args:
            terraform_backend_l3_config__dict (dict[str, Any]): The terraform backend stack configuration dictionary.
        """
        config = TerraformBackendStackConfig.from_dict(terraform_backend_l3_config__dict)
        assert isinstance(config.backend_local_config, BackendLocalConfig)
        assert isinstance(config.provider_azurerm_config, ProviderAzurermConfig)
        assert isinstance(config.constructs_config, TerraformBackendL3Config)


@pytest.fixture(name="stack__terraform_backend_l3_config__instance")
def fixture__stack__terraform_backend_l3_config__instance(
    terraform_backend_l3_config__instance: TerraformBackendL3Config,
) -> TerraformBackendStackConfig:
    """
    Fixture that provides a default configuration for TerraformBackendL1.

    Returns:
        TerraformBackendL1Config: A default configuration instance.
    """
    return TerraformBackendStackConfig(
        backend_local_config=BackendLocalConfig(
            path="test/local/path",
        ),
        provider_azurerm_config=ProviderAzurermConfig(
            tenant_id="test-tenant-id",
            subscription_id="test-sub-id",
            client_id="test-client-id",
            client_secret="test-client-secret",
        ),
        constructs_config=terraform_backend_l3_config__instance,
    )


class TestTerraformBackendL1:
    """
    Test suite for the TerraformBackendStack stack.
    """

    def test__terraform_backend_stack__creation(
        self, stack__terraform_backend_l3_config__instance: TerraformBackendStackConfig
    ) -> None:
        """TODO"""
        app = App()
        stack = TerraformBackendStack(app, "test-stack", env="dev", config=stack__terraform_backend_l3_config__instance)
        synthesized = Testing.synth(stack)
        # There is no function to test terraform backend configuration
        print(synthesized)
        # provider
        assert Testing.to_have_provider_with_properties(
            synthesized,
            AzurermProvider.TF_RESOURCE_TYPE,
            {
                "tenant_id": "test-tenant-id",
                "subscription_id": "test-sub-id",
                "client_id": "test-client-id",
                "client_secret": "test-client-secret",
                "features": [{}],
            },
        )

        # resource group
        assert Testing.to_have_resource_with_properties(
            received=synthesized,
            resource_type=ResourceGroup.TF_RESOURCE_TYPE,
            properties={
                "name": "rg-test-dev-gwc-01",
                "location": "germany west central",
            },
        )

        # # rg lock
        # assert Testing.to_have_resource_with_properties(
        #     received=synthesized,
        #     resource_type=ManagementLock.TF_RESOURCE_TYPE,
        #     properties={
        #         "name": "rg-init-dev-gwc-01-lock",
        #         "lock_level": "CanNotDelete",
        #         "notes": "Test notes.",
        #     },
        # )

        # # storage account
        # assert Testing.to_have_resource_with_properties(
        #     received=synthesized,
        #     resource_type=StorageAccount.TF_RESOURCE_TYPE,
        #     properties={
        #         "name": "sainitdevgwc01",
        #         "location": "germany west central",
        #         # "resource_group_name": "", # cannot be tested as its dynamic in terraform hcl
        #         "account_replication_type": "LRS",
        #         "account_kind": "StorageV2",
        #         "account_tier": "Standard",
        #         "cross_tenant_replication_enabled": False,
        #         "access_tier": "Hot",
        #         "shared_access_key_enabled": False,
        #         "public_network_access_enabled": True,
        #         "is_hns_enabled": False,
        #         "local_user_enabled": False,
        #         "infrastructure_encryption_enabled": True,
        #         "sftp_enabled": False,
        #         "blob_properties": {"delete_retention_policy": {"days": 7}},
        #     },
        # )

        # # storage account lock
        # assert Testing.to_have_resource_with_properties(
        #     received=synthesized,
        #     resource_type=ManagementLock.TF_RESOURCE_TYPE,
        #     properties={
        #         "name": "sainitdevgwc01-lock",
        #         "lock_level": "CanNotDelete",
        #         "notes": "Test notes.",
        #     },
        # )

        # # container
        # assert Testing.to_have_resource_with_properties(
        #     received=synthesized,
        #     resource_type=StorageContainer.TF_RESOURCE_TYPE,
        #     properties={
        #         "name": "test_container",
        #     },
        # )
