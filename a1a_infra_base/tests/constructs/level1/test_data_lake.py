"""
Module for testing the DataLakeL1 and DataLakeL1Config classes.

This module contains unit tests for the DataLakeL1 construct, which is used to create
Azure storage accounts, and the DataLakeL1Config class, which is used to configure
the DataLakeL1 construct.


Tests:
    - TestDataLakeL1Config:
        - test__data_lake_config__from_dict: Tests the from_dict method of the DataLakeL1Config class.
    - TestDataLakeL1:
        - test__data_lake__creation_with_lock: Tests that a DataLakeL1 construct creates a storage account
            with hns enabled.
"""

from typing import Any

import pytest
from cdktf import App, TerraformStack, Testing
from cdktf_cdktf_provider_azurerm.storage_account import StorageAccount

from a1a_infra_base.constants import AzureLocation
from a1a_infra_base.constructs.level1.data_lake import DataLakeL1, DataLakeL1Config


class TestDataLakeL1Config:
    """
    Test suite for the DataLakeL1Config class.
    """

    @pytest.fixture()
    def dict_(self) -> dict[str, Any]:
        """
        Fixture that provides a configuration dictionary for DataLakeL1Config.

        Returns:
            dict[str, Any]: A configuration dictionary.
        """
        return {
            "name": "init",
            "location": "germany west central",
            "sequence_number": "01",
            "account_replication_type": "LRS",
            "account_tier": "Standard",
        }

    def test__data_lake_config__from_dict(self, dict_: dict[str, Any]) -> None:
        """
        Test the from_dict method of the DataLakeL1Config class.

        Args:
            dict_ (dict[str, Any]): The configuration dictionary.
        """
        config = DataLakeL1Config.from_dict(dict_)
        assert config.name == "init"
        assert config.location == AzureLocation.GERMANY_WEST_CENTRAL
        assert config.sequence_number == "01"
        assert config.account_replication_type == "LRS"
        assert config.account_tier == "Standard"
        assert config.is_hns_enabled is True


class TestDataLakeL1:
    """
    Test suite for the DataLakeL1 construct.
    """

    @pytest.fixture()
    def config(self) -> DataLakeL1Config:
        """
        Fixture that provides a default configuration for DataLakeL1.

        Returns:
            DataLakeL1Config: A default configuration instance.
        """
        return DataLakeL1Config(
            name="init",
            location=AzureLocation.GERMANY_WEST_CENTRAL,
            sequence_number="01",
            account_replication_type="LRS",
            account_tier="Standard",
            is_hns_enabled=True,
        )

    def test__data_lake__creation_with_lock(self, config: DataLakeL1Config) -> None:
        """
        Test that a DataLakeL1 construct creates a storage account with a management lock.

        Args:
            config (DataLakeL1Config): The configuration for the storage account with a management lock.
        """
        app = App()
        stack = TerraformStack(app, "test-stack")
        DataLakeL1(stack, "test-account", env="dev", config=config, resource_group_name="test")
        synthesized = Testing.synth(stack)
        assert Testing.to_have_resource_with_properties(
            received=synthesized,
            resource_type=StorageAccount.TF_RESOURCE_TYPE,
            properties={
                "name": "sainitdevgwc01",
                "location": "germany west central",
                "resource_group_name": "test",
                "account_replication_type": "LRS",
                "account_tier": "Standard",
                "is_hns_enabled": True,
            },
        )
