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
from a1a_infra_base.stacks.terraform_backend import TerraformBackendStack

logger: logging.Logger = setup_logger(__name__)

ENV: Final[str] = "env"
STACKS: Final[str] = "stacks"

TERRAFORM_BACKEND_KEY: Final[str] = "terraform_backend"
ENABLED_KEY: Final[str] = "enabled"

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

    env: str = config[ENV]
    stacks: list[dict[str, Any]] = config[STACKS]

    for stack in stacks:
        if TERRAFORM_BACKEND_KEY in stack:
            stack_terraform_backend: dict[str, Any] = stack[TERRAFORM_BACKEND_KEY]
            enabled_cfg: bool = stack_terraform_backend[ENABLED_KEY]
            if not enabled_cfg:
                logger.info("Terraform backend stack is disabled.")
                break

            TerraformBackendStack.from_config(app, "terraform-backend", env=env, config=stack_terraform_backend)

    app.synth()
    logger.info("Application finished.")
