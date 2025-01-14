"""
Module terraform_backend_stack

This module defines the TerraformBackendStack class, which initializes the Terraform stack
with a local backend, an Azure provider, and creates a resource group and a locked storage account.

Classes:
    TerraformBackendStack: A Terraform stack that sets up the local backend, Azure provider,
                           and creates a resource group and a locked storage account.
    TerraformBackendStackConfig: A configuration class for TerraformBackendStack.
"""

import logging
from dataclasses import dataclass
from typing import Any, Self

from cdktf import LocalBackend, TerraformStack
from cdktf_cdktf_provider_azurerm.provider import AzurermProvider

from a1a_infra_base.constructs.level2.terraform_backend import (
    TERRAFORM_BACKEND_L2_KEY,
    TerraformBackendL2,
    TerraformBackendL2Config,
)
from a1a_infra_base.logger import setup_logger
from a1a_infra_base.stacks.stack_abc import (
    AZURERM_KEY,
    BACKEND_KEY,
    CONSTRUCTS_KEY,
    PROVIDER_KEY,
    CombinedMeta,
    StackABC,
    StackConfigABC,
)
from a1a_infra_base.terraform_backend import TerraformBackendLocalConfig
from a1a_infra_base.terraform_provider import TerraformProviderAzurermConfig
from constructs import Construct

logger: logging.Logger = setup_logger(__name__)


@dataclass
class TerraformBackendStackConfig(StackConfigABC):
    """
    A configuration class for TerraformBackendStack.

    This class is responsible for unpacking parameters from a configuration dictionary.

    Attributes:
        backend_local_config (TerraformBackendLocalConfig): The configuration for the Terraform backend.
        provider_azurerm_config (TerraformProviderAzurermConfig): The configuration for the Terraform AzureRM provider.
        constructs_config (TerraformBackendL1Config): The configuration for the Terraform backend L1 construct.
    """

    backend_local_config: TerraformBackendLocalConfig
    provider_azurerm_config: TerraformProviderAzurermConfig
    constructs_config: TerraformBackendL2Config

    @classmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Create a TerraformBackendStackConfig by unpacking parameters from a configuration dictionary.

        Args:
            dict_ (dict): A dictionary containing the stack configuration.

        Returns:
            TerraformBackendStackConfig: A fully-initialized TerraformBackendStackConfig.
        """
        backend_local_config = TerraformBackendLocalConfig.from_dict(dict_[BACKEND_KEY])
        provider_azurerm_config = TerraformProviderAzurermConfig.from_dict(dict_[PROVIDER_KEY][AZURERM_KEY])
        constructs_config = TerraformBackendL2Config.from_dict(dict_[CONSTRUCTS_KEY][TERRAFORM_BACKEND_L2_KEY])

        return cls(
            backend_local_config=backend_local_config,
            provider_azurerm_config=provider_azurerm_config,
            constructs_config=constructs_config,
        )


class TerraformBackendStack(TerraformStack, StackABC, metaclass=CombinedMeta):
    """
    A Terraform stack that sets up the local backend, Azure provider, and creates a resource group
    and a locked storage account based on a given configuration dictionary.

    Attributes:
        terraform_backend_l0 (TerraformBackendL0): The Terraform backend L0 construct.
    """

    def __init__(
        self,
        scope: Construct,
        id_: str = "TerraformBackendStack",
        *,
        env: str,
        config: TerraformBackendStackConfig,
    ) -> None:
        """
        Initializes the TerraformBackendStack construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            config (TerraformBackendStackConfig): The configuration for the Terraform backend stack.
        """
        TerraformStack.__init__(self, scope, id_)

        # Set up the local backend
        LocalBackend(self, path=config.backend_local_config.path)

        # Set up the Azure provider
        AzurermProvider(
            self,
            "AzureRM",
            features=[{}],
            tenant_id=config.provider_azurerm_config.tenant_id,
            subscription_id=config.provider_azurerm_config.subscription_id,
            client_id=config.provider_azurerm_config.client_id,
            client_secret=config.provider_azurerm_config.client_secret,
        )

        # Initialize the TerraformBackendL0 construct
        TerraformBackendL2(
            self,
            "TerraformBackendL0",
            env=env,
            config=config.constructs_config,
        )
