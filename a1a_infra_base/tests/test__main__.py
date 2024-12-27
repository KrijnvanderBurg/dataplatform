"""
Module for testing the StackFactory class and main function.

This module contains unit tests for the StackFactory class, which is used to retrieve
stack configuration and stack classes based on a given configuration dictionary, and the main function.

Tests:
    - TestStackFactory:
        - test_get_stack_valid: Tests that StackFactory.get_stack returns the correct stack classes for a valid
            configuration.
        - test_get_stack_invalid: Tests that StackFactory.get_stack raises a ValueError for an invalid configuration.
        - test_get_stack_disabled: Tests that StackFactory.get_stack returns None for a disabled configuration.
    - TestMainFunction:
        - test_main_function: Tests the main function with a valid configuration file.
"""

from typing import Any

import pytest

from a1a_infra_base.__main__ import ENABLED_KEY, NAME_KEY, TERRAFORM_BACKEND_KEY, StackFactory
from a1a_infra_base.stacks.terraform_backend import TerraformBackendStack, TerraformBackendStackConfig


class TestStackFactory:
    """
    Test suite for the StackFactory class.
    """

    @pytest.fixture()
    def valid_dict(self) -> dict[str, Any]:
        """
        Fixture that provides a valid configuration dictionary for StackFactory.

        Returns:
            dict[str, Any]: A valid configuration dictionary.
        """
        return {
            NAME_KEY: TERRAFORM_BACKEND_KEY,
            ENABLED_KEY: True,
        }

    @pytest.fixture()
    def invalid_dict(self) -> dict[str, Any]:
        """
        Fixture that provides an invalid configuration dictionary for StackFactory.

        Returns:
            dict[str, Any]: An invalid configuration dictionary.
        """
        return {
            NAME_KEY: "unknown_stack",
            ENABLED_KEY: True,
        }

    @pytest.fixture()
    def disabled_dict(self) -> dict[str, Any]:
        """
        Fixture that provides a disabled configuration dictionary for StackFactory.

        Returns:
            dict[str, Any]: A disabled configuration dictionary.
        """
        return {
            NAME_KEY: TERRAFORM_BACKEND_KEY,
            ENABLED_KEY: False,
        }

    def test_get_stack_valid(self, valid_dict: dict[str, Any]) -> None:
        """
        Test that StackFactory.get_stack returns the correct stack classes for a valid configuration.

        Args:
            valid_dict (dict[str, Any]): The valid configuration dictionary.
        """
        stack_result = StackFactory.get_stack(valid_dict)
        assert stack_result is not None
        stack_config_cls, stack_cls = stack_result
        assert stack_config_cls == TerraformBackendStackConfig
        assert stack_cls == TerraformBackendStack

    def test_get_stack_invalid(self, invalid_dict: dict[str, Any]) -> None:
        """
        Test that StackFactory.get_stack raises a ValueError for an invalid configuration.

        Args:
            invalid_dict (dict[str, Any]): The invalid configuration dictionary.
        """
        with pytest.raises(ValueError):
            StackFactory.get_stack(invalid_dict)

    def test_get_stack_disabled(self, disabled_dict: dict[str, Any]) -> None:
        """
        Test that StackFactory.get_stack returns None for a disabled configuration.

        Args:
            disabled_dict (dict[str, Any]): The disabled configuration dictionary.
        """
        stack = StackFactory.get_stack(disabled_dict)
        assert stack is None


# class TestMainFunction:
#     """
#     Test suite for the main function.
#     """

#     @pytest.fixture()
#     def config_content(self) -> str:
#         """
#         Fixture that provides a valid configuration file content.

#         Returns:
#             str: A valid configuration file content.
#         """
#         return json.dumps(
#             {
#                 "env": "dev",
#                 "stacks": [
#                     {
#                         NAME_KEY: TERRAFORM_BACKEND_KEY,
#                         ENABLED_KEY: True,
#                     }
#                 ],
#             }
#         )

#     def test_main_function(self, config_content: str) -> None:
#         """
#         Test the main function with a valid configuration file.

#         Args:
#             config_content (str): The valid configuration file content.
#         """
#         with (
#             patch("builtins.open", new_callable=mock_open) as mock_open_func,
#             patch("a1a_infra_base.__main__.App.synth") as mock_synth,
#             patch("a1a_infra_base.__main__.App") as mock_app_class,
#             patch("a1a_infra_base.__main__.StackFactory.get_stack") as mock_get_stack,
#             patch("a1a_infra_base.stacks.terraform_backend.TerraformBackendStackConfig.from_dict") as mock_from_dict,
#             patch("a1a_infra_base.stacks.terraform_backend.TerraformBackendStack") as mock_stack_cls,
#         ):
#             mock_open_func.return_value.read.return_value = config_content
#             mock_get_stack.return_value = (mock_from_dict, mock_stack_cls)

#             main(config_filepath=Path("/fake/path/to/config.json"))

#             mock_open_func.assert_called_once_with(file=Path("/fake/path/to/config.json"), mode="r", encoding="utf-8")
#             mock_app_class.assert_called_once()
#             mock_synth.assert_called_once()
#             mock_get_stack.assert_called_once()
#             mock_from_dict.assert_called_once()
#             mock_stack_cls.assert_called_once()
