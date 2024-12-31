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
from a1a_infra_base.stacks.terraform_backend import TerraformBackendStack, TerraformBackendStackConfig

logger: logging.Logger = setup_logger(__name__)

ENV_KEY: Final[str] = "env"
STACKS_KEY: Final[str] = "stacks"

TERRAFORM_BACKEND_KEY: Final[str] = "terraform_backend"

NAME_KEY: Final[str] = "name"
ENABLED_KEY: Final[str] = "enabled"


MAPPING_STACKS: Final[dict[str, Any]] = {
    TERRAFORM_BACKEND_KEY: (TerraformBackendStackConfig, TerraformBackendStack),
}

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
        name_cfg: str = stack[NAME_KEY]
        if name_cfg not in MAPPING_STACKS:
            raise ValueError(f"Unknown stack name: {name_cfg}")

        stack_config_cls, stack_cls = MAPPING_STACKS[name_cfg]
        enabled_cfg: bool = stack[ENABLED_KEY]
        if not enabled_cfg:
            logger.info("Stack %s is disabled.", name_cfg)
            break

        stack_config = stack_config_cls.from_dict(dict_=stack)
        stack_cls.from_config(app, name_cfg, env=env, config=stack_config)

    app.synth()
    logger.info("Application finished.")
