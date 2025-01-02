"""
Main module for the a1a_infra_base application.

This module initializes the CDKTF application and synthesizes the Terraform backend stack.
"""

import argparse
import json
import logging
from pathlib import Path
from typing import Any, Final

from cdktf import App

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
    def get_stack(dict_: dict[str, Any]) -> tuple[type[StackConfigABC], type[StackABC]]:
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

        return StackFactory.MAPPING_STACKS[name_cfg]


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

    config_filepath = Path(args.config_filepath)

    try:
        with open(file=config_filepath, mode="r", encoding="utf-8") as f:
            config: dict[str, Any] = json.load(f)
        logger.info("Loaded configuration from %s", config_filepath)
        logger.debug("Configuration content from %s: %s", config_filepath, json.dumps(config, indent=2))
    except Exception as e:
        logger.error("Failed to load configuration from %s: %s", config_filepath, e)
        raise

    app = App()

    env: str = config[ENV_KEY]
    stacks: list[dict[str, Any]] = config[STACKS_KEY]

    for stack in stacks:
        stack_config_cls, stack_cls = StackFactory.get_stack(dict_=stack)
        stack_config = stack_config_cls.from_dict(dict_=stack)
        stack_cls(app, "test", env=env, config=stack_config)  # type: ignore

    app.synth()
    logger.info("Application finished.")
