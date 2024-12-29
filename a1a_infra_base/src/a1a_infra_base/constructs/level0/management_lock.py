"""
Module management_lock

This module defines the ManagementLockL0 class and the ManagementLockL0Config class,
which are responsible for creating and managing a management lock for Azure resources.

Classes:
    ManagementLockL0: A level 0 construct that creates and manages a management lock.
    ManagementLockL0Config: A configuration class for ManagementLockL0.
"""

import logging
from dataclasses import dataclass
from typing import Any, Final, Self

from cdktf_cdktf_provider_azurerm.management_lock import ManagementLock
from constructs import Construct

from a1a_infra_base.constants import AzureResource
from a1a_infra_base.constructs.construct_abc import ConstructL0ABC
from a1a_infra_base.logger import setup_logger

logger: logging.Logger = setup_logger(__name__)

# Constants for dictionary keys
LOCK_LEVEL_KEY: Final[str] = "lock_level"
NOTES_KEY: Final[str] = "notes"


@dataclass
class ManagementLockL0Config(ConstructL0ABC):
    """
    A configuration class for ManagementLockL0.

    Attributes:
        env (str): The environment name.
        lock_level (str): The lock level for the management lock.
        notes (str): Notes for the management lock.
    """

    env: str
    lock_level: str
    notes: str

    @property
    def full_name(self) -> str:
        """Generates the full name for the management lock."""
        return f"-{AzureResource.MANAGEMENT_LOCK.abbr}"

    @classmethod
    def from_config(cls, env: str, config: dict[str, Any]) -> Self:
        """
        Create a ManagementLockL0Config by unpacking parameters from a configuration dictionary.

        Expected format of 'config':
        {
            "lock_level": "<lock level>",
            "notes": "<notes>"
        }

        Args:
            env (str): The environment name.
            config (dict): A dictionary containing management lock configuration.

        Returns:
            ManagementLockL0Config: A fully-initialized ManagementLockL0Config.
        """
        lock_level = config[LOCK_LEVEL_KEY]
        notes = config[NOTES_KEY]
        return cls(env=env, lock_level=lock_level, notes=notes)


class ManagementLockL0(Construct):
    """
    A level 0 construct that creates and manages a management lock for Azure resources.

    Attributes:
        management_lock (ManagementLock): The management lock applied to the resource.
    """

    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        name: str,
        resource_id: str,
        config: ManagementLockL0Config,
    ) -> None:
        """
        Initializes the ManagementLockL0 construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            name (str): The name of the resource to which the lock is applied.
            resource_id (str): The ID of the resource to which the lock is applied.
            config (ManagementLockL0Config): The configuration for the management lock.
        """
        super().__init__(scope, id_)

        self._management_lock = ManagementLock(
            self,
            config.full_name,
            name=f"{name}{config.full_name}",
            scope=resource_id,
            lock_level=config.lock_level,
            notes=config.notes,
        )

    @property
    def management_lock(self) -> ManagementLock:
        """Gets the management lock applied to the resource."""
        return self._management_lock
