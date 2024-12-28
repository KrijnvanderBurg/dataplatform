"""
Module storage_account_locked

This module defines the StorageAccountLockedL1 class, which is responsible for creating
and managing a locked Azure storage account with specific configurations.

Classes:
    StorageAccountLockedL1: A level 1 construct that creates and manages a locked Azure storage account.
"""

from typing import Any, Final, Self

from constructs import Construct

from a1a_infra_base.constructs.level0.management_lock import ManagementLockL0
from a1a_infra_base.constructs.level0.resource_group import ResourceGroupL0
from a1a_infra_base.constructs.level0.storage_account import StorageAccountL0

# Constants for dictionary keys
NAME_KEY: Final[str] = "name"
LOCATION_KEY: Final[str] = "location"
SEQUENCE_NUMBER_KEY: Final[str] = "sequence_number"
RESOURCE_GROUP_NAME_KEY: Final[str] = "resource_group_name"
ACCOUNT_REPLICATION_TYPE_KEY: Final[str] = "account_replication_type"
ACCOUNT_KIND_KEY: Final[str] = "account_kind"
ACCOUNT_TIER_KEY: Final[str] = "account_tier"
CROSS_TENANT_REPLICATION_ENABLED_KEY: Final[str] = "cross_tenant_replication_enabled"
ACCESS_TIER_KEY: Final[str] = "access_tier"
SHARED_ACCESS_KEY_ENABLED_KEY: Final[str] = "shared_access_key_enabled"
PUBLIC_NETWORK_ACCESS_ENABLED_KEY: Final[str] = "public_network_access_enabled"
IS_HNS_ENABLED_KEY: Final[str] = "is_hns_enabled"
LOCAL_USER_ENABLED_KEY: Final[str] = "local_user_enabled"
INFRASTRUCTURE_ENCRYPTION_ENABLED_KEY: Final[str] = "infrastructure_encryption_enabled"
SFTP_ENABLED_KEY: Final[str] = "sftp_enabled"
BLOB_PROPERTIES_KEY: Final[str] = "blob_properties"
LOCK_LEVEL_KEY: Final[str] = "lock_level"
MANAGEMENT_LOCK_KEY: Final[str] = "management_lock"


class StorageAccountLockedL1(Construct):
    """
    A level 1 construct that creates and manages a locked Azure storage account.

    Attributes:
        storage_account (StorageAccountL0): The Azure storage account.
        management_lock (ManagementLockL0): The management lock applied to the storage account.
    """

    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        storage_account: StorageAccountL0,
        management_lock: ManagementLockL0,
    ) -> None:
        """
        Initializes the StorageAccountLockedL1 construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            storage_account (StorageAccountL0): The storage account level 0 construct.
            management_lock (ManagementLockL0): The management lock level 0 construct.
        """
        super().__init__(scope, id_)

        self._storage_account = storage_account
        self._management_lock = management_lock

    @property
    def storage_account(self) -> StorageAccountL0:
        """Gets the Azure storage account."""
        return self._storage_account

    @property
    def management_lock(self) -> ManagementLockL0:
        """Gets the management lock applied to the storage account."""
        return self._management_lock

    @classmethod
    def from_config(
        cls, scope: Construct, id_: str, env: str, config: dict[str, Any], resource_group_l0: ResourceGroupL0
    ) -> Self:
        """
        Create a StorageAccountLockedL1 construct by unpacking parameters from a configuration dictionary.

        Expected format of 'config':
        {
            "name": "<storage account name>",
            "location": "<AzureLocation enum value name>",
            "sequence_number": "<sequence number>",
            "resource_group_name": "<resource group name>",
            "account_replication_type": "<replication type>",
            "account_kind": "<account kind>",
            "account_tier": "<account tier>",
            "cross_tenant_replication_enabled": <bool>,
            "access_tier": "<access tier>",
            "shared_access_key_enabled": <bool>,
            "public_network_access_enabled": <bool>,
            "is_hns_enabled": <bool>,
            "local_user_enabled": <bool>,
            "infrastructure_encryption_enabled": <bool>,
            "sftp_enabled": <bool>,
            "blob_properties": {
                "delete_retention_policy": {
                    "delete_retention_days": <int>
                }
            },
            "management_lock": {
                "lock_level": "<lock level>"
                "notes": "<notes>"
            }
        }

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            config (dict): A dictionary containing storage account configuration.
            resource_group_l0 (ResourceGroupL0): The resource group level 0 construct.

        Returns:
            StorageAccountLockedL1: A fully-initialized StorageAccountLockedL1 construct.
        """
        storage_account = StorageAccountL0.from_config(
            scope, "StorageAccountConstruct", config=config, env=env, resource_group_l0=resource_group_l0
        )
        management_lock = ManagementLockL0.from_config(
            scope,
            "ManagementLockConstruct",
            config=config[MANAGEMENT_LOCK_KEY],
            resource_id=storage_account.storage_account.id,
        )

        return cls(scope=scope, id_=id_, storage_account=storage_account, management_lock=management_lock)
