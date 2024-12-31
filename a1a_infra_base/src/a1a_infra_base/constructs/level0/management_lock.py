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
from a1a_infra_base.constructs.construct_abc import AttachedConstructABC, CombinedMeta, ConstructConfigABC
from a1a_infra_base.logger import setup_logger

logger: logging.Logger = setup_logger(__name__)

# Constants for dictionary keys
NAME_KEY: Final[str] = "name"
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

    name: str
    lock_level: str
    notes: str

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
            dict_ (dict): A dictionary containing management lock configuration.

        Returns:
            ManagementLockL0Config: A fully-initialized ManagementLockL0Config.
        """
        name = dict_[NAME_KEY]
        lock_level = dict_[LOCK_LEVEL_KEY]
        notes = dict_[NOTES_KEY]
        return cls(name=name, lock_level=lock_level, notes=notes)


class ManagementLockL0(Construct, AttachedConstructABC[ManagementLockL0Config], metaclass=CombinedMeta):
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
        resource_id: str,
        config: ManagementLockL0Config,
    ) -> None:
        """
        Initializes the ManagementLockL0 construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            resource_id (str): The resource ID to attach to.
            config (ManagementLockL0Config): The configuration for the management lock.
        """
        super().__init__(scope, id_)

        self.full_name = f"{config.name}-{AzureResource.MANAGEMENT_LOCK.abbr}"
        self._management_lock = ManagementLock(
            self,
            self.full_name,
            name=self.full_name,
            scope=resource_id,
            lock_level=config.lock_level,
            notes=config.notes,
        )

    @property
    def management_lock(self) -> ManagementLock:
        """Gets the management lock applied to the resource."""
        return self._management_lock

    @classmethod
    def from_config(
        cls, scope: Construct, id_: str, env: str, attach_to_resource_id: str, config: ManagementLockL0Config
    ) -> Self:
        """
        Create a ManagementLockL0 instance from a ManagementLockL0Config object.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            attach_to_resource_id (str): The resource ID to attach to.
            config (ManagementLockL0Config): The configuration object for the management lock.

        Returns:
            ManagementLockL0: A fully-initialized ManagementLockL0 instance.
        """
        return cls(scope, id_, _=env, resource_id=attach_to_resource_id, config=config)
