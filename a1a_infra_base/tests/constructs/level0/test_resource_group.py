"""
Module for testing the ResourceGroupL0 and ResourceGroupL0Config classes.

This module contains unit tests for the ResourceGroupL0 construct, which is used to create
Azure resource groups with optional management locks, and the ResourceGroupL0Config class,
which is used to configure the ResourceGroupL0 construct.


Tests:
    - TestResourceGroupL0Config:
        - test__resource_group_config__from_dict: Tests the from_dict method of the ResourceGroupL0Config class.
    - TestResourceGroupL0:
        - test__resource_group__creation_with_lock: Tests that a ResourceGroupL0 construct creates an Azure resource
            group with a management lock.
        - test__resource_group__creation_without_lock: Tests that a ResourceGroupL0 construct creates an Azure resource
            group without a management lock.
"""

from typing import Any

import pytest
from cdktf import App, TerraformStack, Testing
from cdktf_cdktf_provider_azurerm.management_lock import ManagementLock
from cdktf_cdktf_provider_azurerm.resource_group import ResourceGroup

from a1a_infra_base.constants import AzureLocation
from a1a_infra_base.constructs.level0.management_lock import ManagementLockL0Config
from a1a_infra_base.constructs.level0.resource_group import ResourceGroupL0, ResourceGroupL0Config


class TestResourceGroupL0Config:
    """
    Test suite for the ResourceGroupL0Config class.
    """

    @pytest.fixture()
    def dict_(self) -> dict[str, Any]:
        """
        Fixture that provides a configuration dictionary for ResourceGroupL0Config.

        Returns:
            dict[str, Any]: A configuration dictionary.
        """
        return {
            "name": "init",
            "location": "germany west central",
            "sequence_number": "01",
            "management_lock_l0": {
                "lock_level": "CanNotDelete",
                "notes": "Required for Terraform deployments.",
            },
        }

    def test__resource_group_config__from_dict(self, dict_: dict[str, Any]) -> None:
        """
        Test the from_dict method of the ResourceGroupL0Config class.

        Args:
            dict_ (dict[str, Any]): The configuration dictionary.
        """
        config = ResourceGroupL0Config.from_dict(dict_)
        assert config.name == "init"
        assert config.location == AzureLocation.GERMANY_WEST_CENTRAL
        assert config.sequence_number == "01"
        assert config.management_lock_l0 is not None
        assert config.management_lock_l0.lock_level == "CanNotDelete"
        assert config.management_lock_l0.notes == "Required for Terraform deployments."  # type: ignore


class TestResourceGroupL0:
    """
    Test suite for the ResourceGroupL0 construct.
    """

    @pytest.fixture()
    def config(self) -> ResourceGroupL0Config:
        """
        Fixture that provides a default configuration for ResourceGroupL0.

        Returns:
            ResourceGroupL0Config: A default configuration instance.
        """
        return ResourceGroupL0Config(
            name="test",
            location=AzureLocation.GERMANY_WEST_CENTRAL,
            sequence_number="01",
            management_lock_l0=ManagementLockL0Config(lock_level="CanNotDelete", notes="Test lock"),
        )

    def test__resource_group__creation_with_lock(self, config: ResourceGroupL0Config) -> None:
        """
        Test that a ResourceGroupL0 construct creates an Azure resource group with a management lock.

        Args:
            config (ResourceGroupL0Config): The configuration for the resource group with a management lock.
        """
        app = App()
        stack = TerraformStack(app, "test-stack")
        ResourceGroupL0(stack, "test", env="dev", config=config)
        synthesized = Testing.synth(stack)
        assert Testing.to_have_resource_with_properties(
            received=synthesized,
            resource_type=ResourceGroup.TF_RESOURCE_TYPE,
            properties={
                "name": "rg-test-dev-gwc-01",
                "location": "germany west central",
            },
        )
        assert Testing.to_have_resource_with_properties(
            received=synthesized,
            resource_type=ManagementLock.TF_RESOURCE_TYPE,
            properties={
                "name": "rg-test-dev-gwc-01-lock",
                "lock_level": "CanNotDelete",
                "notes": "Test lock",
            },
        )
        # assert Testing.to_be_valid_terraform(synthesized)

    def test__resource_group__creation_without_lock(self, config: ResourceGroupL0Config) -> None:
        """
        Test that a ResourceGroupL0 construct creates an Azure resource group without a management lock.

        Args:
            config (ResourceGroupL0Config): The configuration for the resource group without a management lock.
        """
        config.management_lock_l0 = None
        app = App()
        stack = TerraformStack(app, "test-stack")
        ResourceGroupL0(stack, "test", env="dev", config=config)
        synthesized = Testing.synth(stack)
        assert Testing.to_have_resource_with_properties(
            received=synthesized,
            resource_type=ResourceGroup.TF_RESOURCE_TYPE,
            properties={
                "name": "rg-test-dev-gwc-01",
                "location": "germany west central",
            },
        )
        assert not Testing.to_have_resource_with_properties(
            received=synthesized,
            resource_type=ManagementLock.TF_RESOURCE_TYPE,
            properties={
                "name": "rg-test-dev-gwc-01-lock",
            },
        )
        # assert Testing.to_be_valid_terraform(synthesized)
