"""
Module management_lock

This module defines the ManagementLockL0 class, which is responsible for creating
and managing a management lock for Azure resources.

Classes:
    ManagementLockL0: A level 0 construct that creates and manages a management lock.
"""

from typing import Any, Final, Self

from cdktf_cdktf_provider_azurerm.management_lock import ManagementLock
from constructs import Construct

from a1a_infra_base.constants import AzureResource

# Constants for dictionary keys
LOCK_LEVEL_KEY: Final[str] = "lock_level"
NOTES_KEY: Final[str] = "notes"


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
        resource_id: str,
        lock_level: str,
        notes: str,
    ) -> None:
        """
        Initializes the ManagementLockL0 construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            resource_id (str): The ID of the resource to which the lock is applied.
            lock_level (str): The lock level for the management lock.
            notes (str): Notes for the management lock.
        """
        super().__init__(scope, id_)

        self._management_lock = ManagementLock(
            self,
            f"{resource_id}_{AzureResource.MANAGEMENT_LOCK.abbr}",
            name=f"{resource_id}-{AzureResource.MANAGEMENT_LOCK.abbr}",
            scope=resource_id,
            lock_level=lock_level,
            notes=notes,
        )

    @property
    def management_lock(self) -> ManagementLock:
        """Gets the management lock applied to the resource."""
        return self._management_lock

    @classmethod
    def from_config(cls, scope: Construct, id_: str, config: dict[str, Any], resource_id: str) -> Self:
        """
        Create a ManagementLockL0 construct by unpacking parameters from a configuration dictionary.

        Expected format of 'config':
        {
            "lock_level": "<lock level>",
            "notes": "<notes>"
        }

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            config (dict): A dictionary containing management lock configuration.
            resource_id (str): The ID of the resource to which the lock is applied.

        Returns:
            ManagementLockL0: A fully-initialized ManagementLockL0 construct.
        """
        lock_level = config[LOCK_LEVEL_KEY]
        notes = config.get(NOTES_KEY, "")

        return cls(scope=scope, id_=id_, resource_id=resource_id, lock_level=lock_level, notes=notes)
