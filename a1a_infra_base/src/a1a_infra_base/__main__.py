"""
Main module for the a1a_infra_base application.

This module initializes the CDKTF application and synthesizes the Terraform backend stack.
"""

import argparse
import logging
from pathlib import Path
from typing import Any, Final

from cdktf import App

from a1a_infra_base.file import FileHandlerFactory
from a1a_infra_base.logger import setup_logger
from a1a_infra_base.stacks.stack_abc import StackABC, StackConfigABC
from a1a_infra_base.stacks.terraform_backend import TerraformBackendStack, TerraformBackendStackConfig

logger: logging.Logger = setup_logger(__name__)

ENV_KEY: Final[str] = "env"
STACKS_KEY: Final[str] = "stacks"

NAME_KEY: Final[str] = "name"
ENABLED_KEY: Final[str] = "enabled"

TERRAFORM_BACKEND_KEY: Final[str] = "terraform_backend"


class StackFactory:
    """
    Factory class for creating stacks.
    """

    MAPPING_STACKS: Final[dict[str, tuple[type[StackConfigABC], type[StackABC]]]] = {
        TERRAFORM_BACKEND_KEY: (TerraformBackendStackConfig, TerraformBackendStack),
    }

    @staticmethod
    def get_stack(dict_: dict[str, Any]) -> tuple[type[StackConfigABC], type[StackABC]] | None:
        """
        Create a stack by unpacking parameters from a stack configuration dictionary.

        Args:
            dict_ (dict[str, Any]): The configuration for the stack.

        Returns:
            StackABC: A fully-initialized stack.
        """
        name_cfg: str = dict_[NAME_KEY]
        if name_cfg not in StackFactory.MAPPING_STACKS:
            raise ValueError(f"Unknown stack name: {name_cfg}")

        enabled_cfg: bool = dict_[ENABLED_KEY]
        if not enabled_cfg:
            logger.info("Stack %s is disabled.", name_cfg)
            return None

        return StackFactory.MAPPING_STACKS[name_cfg]


def main(config_filepath: Path) -> None:
    """
    Main function to load configuration, initialize the application, and synthesize the app.

    Args:
        config_filepath (Path): The file path to the configuration file.

    Raises:
        Exception: If there is an error loading the configuration file.
    """
    app = App()

    dict_: dict[str, Any] = FileHandlerFactory.create(filepath=str(config_filepath)).read()
    env: str = dict_[ENV_KEY]
    stacks: list[dict[str, Any]] = dict_[STACKS_KEY]

    for stack in stacks:
        stack_result = StackFactory.get_stack(dict_=stack)
        if stack_result is None:
            break
        stack_config_cls, stack_cls = stack_result
        stack_config = stack_config_cls.from_dict(dict_=stack)
        stack_cls(app, "test", env=env, config=stack_config)  # type: ignore

    app.synth()
    logger.info("Application finished.")


if __name__ == "__main__":
    logger.info("Starting application...")

    parser = argparse.ArgumentParser(description="a1a_infra_base")
    parser.add_argument(
        "--config-filepath",
        required=True,
        type=str,
        help="Path to config file.",
    )

    args: argparse.Namespace = parser.parse_args()
    logger.info("Parsed arguments: %s", args)

    main(config_filepath=Path(args.config_filepath))
