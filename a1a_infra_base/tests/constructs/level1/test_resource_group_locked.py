"""
Module for testing the ResourceGroupLockedL1 and ResourceGroupLockedL1Config classes.

This module contains unit tests for the ResourceGroupLockedL1 construct, which is used to create
Azure resource groups with optional management locks, and the ResourceGroupLockedL1Config class,
which is used to configure the ResourceGroupLockedL1 construct.


Tests:
    - TestResourceGroupLockedL1Config:
        - test__resource_group_config__from_dict: Tests the from_dict method of the ResourceGroupLockedL1Config class.
    - TestResourceGroupLockedL1:
        - test__resource_group__creation: Tests that a ResourceGroupLockedL1 construct creates an Azure resource
            group with a management lock.
"""

from typing import Any

import pytest
from cdktf import App, TerraformStack, Testing
from cdktf_cdktf_provider_azurerm.management_lock import ManagementLock
from cdktf_cdktf_provider_azurerm.resource_group import ResourceGroup

from a1a_infra_base.constructs.level0.management_lock import ManagementLockL0Config
from a1a_infra_base.constructs.level0.resource_group import ResourceGroupL0Config
from a1a_infra_base.constructs.level1.resource_group_secure import ResourceGroupLockedL1, ResourceGroupLockedL1Config


@pytest.fixture(name="resource_group_locked_l1_config__dict")
def fixture__resource_group_locked_l1_config__dict(
    resource_group_l0_config__dict: dict[str, Any],
    management_lock_l0_config__dict: dict[str, Any],
) -> dict[str, Any]:
    """
    Fixture that provides a configuration dictionary for ResourceGroupLockedL1Config.

    Returns:
        dict[str, Any]: A configuration dictionary.
    """
    return {
        "resource_group_l0": resource_group_l0_config__dict,
        "management_lock_l0": management_lock_l0_config__dict,
    }


class TestResourceGroupLockedL1Config:
    """
    Test suite for the ResourceGroupLockedL1Config class.
    """

    def test__resource_group_config__from_dict(self, resource_group_locked_l1_config__dict: dict[str, Any]) -> None:
        """
        Test the from_dict method of the ResourceGroupLockedL1Config class.

        Args:
            resource_group_locked_l1_config__dict (dict[str, Any]): The configuration dictionary.
        """
        config = ResourceGroupLockedL1Config.from_dict(resource_group_locked_l1_config__dict)
        assert isinstance(config.resource_group_l0, ResourceGroupL0Config)
        assert isinstance(config.management_lock_l0, ManagementLockL0Config)


@pytest.fixture(name="resource_group_locked_l1_config__instance")
def fixture__resource_group_locked_l1_config__instance(
    resource_group_l0_config__instance: ResourceGroupL0Config,
    management_lock_l0_config__instance: ManagementLockL0Config,
) -> ResourceGroupLockedL1Config:
    """
    Fixture that provides a default configuration for ResourceGroupLockedL1.

    Returns:
        ResourceGroupLockedL1Config: A default configuration instance.
    """
    return ResourceGroupLockedL1Config(
        resource_group_l0=resource_group_l0_config__instance,
        management_lock_l0=management_lock_l0_config__instance,
    )


class TestResourceGroupLockedL1:
    """
    Test suite for the ResourceGroupLockedL1 construct.
    """

    def test__resource_group__creation(
        self, resource_group_locked_l1_config__instance: ResourceGroupLockedL1Config
    ) -> None:
        """
        Test that a ResourceGroupLockedL1 construct creates an Azure resource group with a management lock.

        Args:
            resource_group_locked_l1_config__instancey67u (ResourceGroupLockedL1Config): The configuration for the resource group with a management lock.
        """
        app = App()
        stack = TerraformStack(app, "test-stack")
        ResourceGroupLockedL1(stack, "test", env="dev", config=resource_group_locked_l1_config__instance)
        synthesized = Testing.synth(stack)

        assert Testing.to_have_resource(
            received=synthesized,
            resource_type=ResourceGroup.TF_RESOURCE_TYPE,
        )

        assert Testing.to_have_resource(
            received=synthesized,
            resource_type=ManagementLock.TF_RESOURCE_TYPE,
        )

        # assert Testing.to_be_valid_terraform(synthesized)
