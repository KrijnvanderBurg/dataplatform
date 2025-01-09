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

from a1a_infra_base.constants import AzureResource
from a1a_infra_base.constructs.construct_abc import CombinedMeta, ConstructConfigABC
from a1a_infra_base.logger import setup_logger
from constructs import Construct

logger: logging.Logger = setup_logger(__name__)

# Constants for dictionary keys
LOCK_LEVEL_KEY: Final[str] = "lock_level"
NOTES_KEY: Final[str] = "notes"


@dataclass
class ManagementLockL0Config(ConstructConfigABC):
    """
    A configuration class for ManagementLockL0.

    Attributes:
        lock_level (str): The lock level for the management lock.
        notes (str): Notes for the management lock.
    """

    lock_level: str
    notes: str | None = None

    @classmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Create a ManagementLockL0Config by unpacking parameters from a configuration dictionary.

        Expected format of 'dict_':
        {
            "lock_level": "<lock level>",
            "notes": "<notes>"
        }

        Args:
            dict_ (dict[str, Any]): A dictionary containing management lock configuration.

        Returns:
            ManagementLockL0Config: A fully-initialized ManagementLockL0Config.
        """
        lock_level = dict_[LOCK_LEVEL_KEY]
        notes = dict_.get(NOTES_KEY, cls.notes)
        return cls(lock_level=lock_level, notes=notes)


class ManagementLockL0(Construct, metaclass=CombinedMeta):
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
        _: str,  # unused env parameter; only present for consistency and to match signature
        config: ManagementLockL0Config,
        resource_id: str,
        resource_name: str,
    ) -> None:
        """
        Initializes the ManagementLockL0 construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            config (ManagementLockL0Config): The configuration for the management lock.
            resource_id (str): The resource ID to attach to.
            resource_name (str): The name of the resource to attach to.
        """
        super().__init__(scope, id_)

        self.full_name = f"{resource_name}-{AzureResource.MANAGEMENT_LOCK.abbr}"
        self._management_lock = ManagementLock(
            self,
            self.full_name,
            name=self.full_name,
            scope=resource_id,
            lock_level=config.lock_level,
            notes=config.notes,
        )
