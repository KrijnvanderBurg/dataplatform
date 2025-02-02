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
from a1a_infra_base.stacks.lake_house import LakeHouseStack, LakeHouseStackConfig

logger: logging.Logger = setup_logger(__name__)

ENV_KEY: Final[str] = "env"
NAME_KEY: Final[str] = "name"
STACK_KEY: Final[str] = "stack"


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

    name: str = dict_[NAME_KEY]
    env: str = dict_[ENV_KEY]
    stack: dict[str, Any] = dict_[STACK_KEY]

    if name == "lake_house":
        data_lake_config: LakeHouseStackConfig = LakeHouseStackConfig.from_dict(dict_=stack)
        LakeHouseStack(app, "LakeHouseStack", env=env, config=data_lake_config)

    # if name == "terraform_backend":
    #     terraform_backend_dict: dict[str, Any] = constructs[TERRAFORM_BACKEND_KEY]
    #     terraform_backend_config: TerraformBackendStackConfig = TerraformBackendStackConfig.from_dict(
    #         dict_=terraform_backend
    #     )
    #     terraform_backend: TerraformBackendStack = TerraformBackendStack(
    #         app, "terraform_backend", env=env, config=terraform_backend_config
    #     )

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
