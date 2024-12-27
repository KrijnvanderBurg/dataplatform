"""
Main module for the a1a_infra_base application.

This module initializes the CDKTF application and synthesizes the Terraform backend stack.
"""

import json
import logging
from argparse import ArgumentParser

from cdktf import App

from a1a_infra_base.constructs.level2.terraform_backend import TerraformBackendStack
from a1a_infra_base.logger import setup_logger

logger: logging.Logger = setup_logger(__name__)


if __name__ == "__main__":
    logger.info("Starting application...")

    parser = ArgumentParser(description="a1a_infra_base")
    parser.add_argument(
        "--config-filepath",
        required=True,
        type=str,
        help="Path to config file.",
    )

    args = parser.parse_args()
    logger.info("Parsed arguments: %s", args)

    try:
        with open(file=args.config_filepath, mode="r", encoding='utf-8') as f:
            config = json.load(f)
        logger.info("Loaded configuration from %s", args.config_filepath)
    except Exception as e:
        logger.error("Failed to load configuration from %s: %s",
                     args.config_filepath, e)
        raise

    logger.debug("Configuration content: %s", json.dumps(config, indent=2))

    app = App()
    try:
        TerraformBackendStack.from_config(
            scope=app,
            id_="terraform-backend",
            config=config
        )
        logger.info("TerraformBackendStack initialized successfully.")
    except Exception as e:
        logger.error("Failed to initialize TerraformBackendStack: %s", e)
        raise

    try:
        app.synth()
        logger.info("Synthesized the Terraform stack successfully.")
    except Exception as e:
        logger.error("Failed to synthesize the Terraform stack: %s", e)
        raise

    logger.info("Application finished.")
