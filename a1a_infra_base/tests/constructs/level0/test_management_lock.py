"""
Module for testing the ManagementLockL0 and ManagementLockL0Config classes.

This module contains unit tests for the ManagementLockL0 construct, which is used to create
management locks for Azure resources, and the ManagementLockL0Config class, which is used to
configure the ManagementLockL0 construct.

Fixtures:
    - TestManagementLockL0Config:
        - dict_: Provides a configuration dictionary for ManagementLockL0Config.
    - TestManagementLockL0:
        - config: Provides a default configuration for ManagementLockL0.
        - stack: Provides a TerraformStack instance.

Tests:
    - TestManagementLockL0Config:
        - test__management_lock_config__from_dict: Tests the from_dict method of the ManagementLockL0Config class.
    - TestManagementLockL0:
        - test__management_lock__creation: Tests that a ManagementLockL0 construct creates a management lock.
"""

import pytest
from cdktf import App, TerraformStack, Testing
from cdktf_cdktf_provider_azurerm.management_lock import ManagementLock

from a1a_infra_base.constructs.level0.management_lock import ManagementLockL0, ManagementLockL0Config


class TestManagementLockL0Config:
    """
    Test suite for the ManagementLockL0Config class.
    """

    @pytest.fixture
    def dict_(self) -> dict:
        """
        Fixture that provides a configuration dictionary for ManagementLockL0Config.

        Returns:
            dict: A configuration dictionary.
        """
        return {
            "lock_level": "CanNotDelete",
            "notes": "Required for Terraform deployments.",
        }

    def test__management_lock_config__from_dict(self, dict_: dict) -> None:
        """
        Test the from_dict method of the ManagementLockL0Config class.

        Args:
            dict_ (dict): The configuration dictionary.
        """
        config = ManagementLockL0Config.from_dict(dict_)
        assert config.lock_level == "CanNotDelete"
        assert config.notes == "Required for Terraform deployments."


class TestManagementLockL0:
    """
    Test suite for the ManagementLockL0 construct.
    """

    @pytest.fixture
    def config(self) -> ManagementLockL0Config:
        """
        Fixture that provides a default configuration for ManagementLockL0.

        Returns:
            ManagementLockL0Config: A default configuration instance.
        """
        return ManagementLockL0Config(
            lock_level="CanNotDelete",
            notes="Test lock",
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

    def test__management_lock__creation(self, stack: TerraformStack, config: ManagementLockL0Config) -> None:
        """
        Test that a ManagementLockL0 construct creates a management lock.

        Args:
            stack (TerraformStack): The Terraform stack.
            config (ManagementLockL0Config): The configuration for the management lock.
        """
        ManagementLockL0(
            stack, "test-lock", _="dev", config=config, resource_name="test-resource", resource_id="test-id"
        )
        synthesized = Testing.synth(stack)
        assert Testing.to_have_resource_with_properties(
            received=synthesized,
            resource_type=ManagementLock.TF_RESOURCE_TYPE,
            properties={
                "name": "test-resource-ml",
                "scope": "test-id",
                "lock_level": "CanNotDelete",
                "notes": "Test lock",
            },
        )
