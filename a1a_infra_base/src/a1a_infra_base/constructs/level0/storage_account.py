"""
Module storage_account

This module defines the StorageAccountL0 class and the StorageAccountConfig class,
which are responsible for creating and managing an Azure storage account with specific configurations.

Classes:
    StorageAccountL0: A level 0 construct that creates and manages an Azure storage account.
    StorageAccountConfig: A configuration class for StorageAccountL0.
"""

import logging
from dataclasses import dataclass
from typing import Any, Final, Self

from cdktf_cdktf_provider_azurerm.storage_account import (
    StorageAccount,
    StorageAccountBlobProperties,
    StorageAccountBlobPropertiesDeleteRetentionPolicy,
)
from constructs import Construct

from a1a_infra_base.constants import AzureLocation, AzureResource
from a1a_infra_base.constructs.construct_abc import ConstructABC
from a1a_infra_base.constructs.level0.management_lock import ManagementLockL0, ManagementLockL0Config
from a1a_infra_base.constructs.level0.resource_group import ResourceGroupL0
from a1a_infra_base.constructs.level0.storage_container import StorageContainerL0, StorageContainerL0Config
from a1a_infra_base.logger import setup_logger

logger: logging.Logger = setup_logger(__name__)

# Constants for dictionary keys
NAME_KEY: Final[str] = "name"
LOCATION_KEY: Final[str] = "location"
SEQUENCE_NUMBER_KEY: Final[str] = "sequence_number"
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
DELETE_RETENTION_POLICY_KEY: Final[str] = "delete_retention_policy"
DELETE_RETENTION_DAYS_KEY: Final[str] = "delete_retention_days"
CONTAINERS_KEY: Final[str] = "containers"
MANAGEMENT_LOCK_KEY: Final[str] = "management_lock"


@dataclass
class DeleteRetentionPolicy:
    """
    A class to represent the delete retention policy configuration.

    Attributes:
        days (int): The number of days to retain deleted items.
    """

    days: int

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> Self:
        """
        Create a DeleteRetentionPolicy instance from a configuration dictionary.

        Args:
            config (dict): A dictionary containing delete retention policy configuration.

        Returns:
            DeleteRetentionPolicy: A fully-initialized DeleteRetentionPolicy instance.
        """
        days = config[DELETE_RETENTION_DAYS_KEY]
        return cls(days)


@dataclass
class BlobProperties:
    """
    A class to represent the blob properties configuration.

    Attributes:
        delete_retention_policy (DeleteRetentionPolicy): The delete retention policy configuration.
    """

    delete_retention_policy: DeleteRetentionPolicy

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> Self:
        """
        Create a BlobProperties instance from a configuration dictionary.

        Args:
            config (dict): A dictionary containing blob properties configuration.

        Returns:
            BlobProperties: A fully-initialized BlobProperties instance.
        """
        delete_retention_policy = DeleteRetentionPolicy.from_config(config[DELETE_RETENTION_POLICY_KEY])
        return cls(delete_retention_policy)


@dataclass
class StorageAccountL0Config(ConstructABC):
    """
    A configuration class for StorageAccountL0.

    Attributes:
        name (str): The name of the storage account.
        location (AzureLocation): The Azure location.
        sequence_number (str): The sequence number.
        account_replication_type (str): The replication type of the storage account.
        account_kind (str): The kind of the storage account.
        account_tier (str): The tier of the storage account.
        cross_tenant_replication_enabled (bool): Whether cross-tenant replication is enabled.
        access_tier (str): The access tier of the storage account.
        shared_access_key_enabled (bool): Whether shared access key is enabled.
        public_network_access_enabled (bool): Whether public network access is enabled.
        is_hns_enabled (bool): Whether hierarchical namespace is enabled.
        local_user_enabled (bool): Whether local user is enabled.
        infrastructure_encryption_enabled (bool): Whether infrastructure encryption is enabled.
        sftp_enabled (bool): Whether SFTP is enabled.
        blob_properties (BlobProperties): The blob properties configuration.
        containers (list[StorageContainerL0Config]): The list of storage containers configuration.
        management_lock: ManagementLockL0Config | None = None
    """

    name: str
    location: AzureLocation
    sequence_number: str
    account_replication_type: str
    account_kind: str
    account_tier: str
    cross_tenant_replication_enabled: bool
    access_tier: str
    shared_access_key_enabled: bool
    public_network_access_enabled: bool
    is_hns_enabled: bool
    local_user_enabled: bool
    infrastructure_encryption_enabled: bool
    sftp_enabled: bool
    blob_properties: BlobProperties
    containers: list[StorageContainerL0Config]
    management_lock: ManagementLockL0Config | None = None

    @classmethod
    def from_dict(cls, config: dict[str, Any]) -> Self:
        """
        Create a StorageAccountConfig by unpacking parameters from a configuration dictionary.

        Expected format of 'config':
        {
            "name": "<storage account name>",
            "location": "<AzureLocation enum value name>",
            "sequence_number": "<sequence number>",
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
            "containers": [
                {
                    "name": "<container name>",
                }
            ],
            "management_lock": {
                "lock_level": "<lock level>",
                "notes": "<notes>"
            }
        }

        Args:
            env (str): The environment name.
            config (dict): A dictionary containing storage account configuration.

        Returns:
            StorageAccountConfig: A fully-initialized StorageAccountConfig.
        """
        name = config[NAME_KEY]
        location = AzureLocation.from_full_name(config[LOCATION_KEY])
        sequence_number = config[SEQUENCE_NUMBER_KEY]
        account_replication_type = config[ACCOUNT_REPLICATION_TYPE_KEY]
        account_kind = config[ACCOUNT_KIND_KEY]
        account_tier = config[ACCOUNT_TIER_KEY]
        cross_tenant_replication_enabled = config[CROSS_TENANT_REPLICATION_ENABLED_KEY]
        access_tier = config[ACCESS_TIER_KEY]
        shared_access_key_enabled = config[SHARED_ACCESS_KEY_ENABLED_KEY]
        public_network_access_enabled = config[PUBLIC_NETWORK_ACCESS_ENABLED_KEY]
        is_hns_enabled = config[IS_HNS_ENABLED_KEY]
        local_user_enabled = config[LOCAL_USER_ENABLED_KEY]
        infrastructure_encryption_enabled = config[INFRASTRUCTURE_ENCRYPTION_ENABLED_KEY]
        sftp_enabled = config[SFTP_ENABLED_KEY]
        blob_properties = BlobProperties.from_config(config[BLOB_PROPERTIES_KEY])

        containers = []
        for container_config in config.get(CONTAINERS_KEY, []):
            containers.append(StorageContainerL0Config.from_dict(config=container_config))

        management_lock = config.get(MANAGEMENT_LOCK_KEY, None)
        if management_lock:
            management_lock = ManagementLockL0Config.from_dict(config=config[MANAGEMENT_LOCK_KEY])

        return cls(
            name=name,
            location=location,
            sequence_number=sequence_number,
            account_replication_type=account_replication_type,
            account_kind=account_kind,
            account_tier=account_tier,
            cross_tenant_replication_enabled=cross_tenant_replication_enabled,
            access_tier=access_tier,
            shared_access_key_enabled=shared_access_key_enabled,
            public_network_access_enabled=public_network_access_enabled,
            is_hns_enabled=is_hns_enabled,
            local_user_enabled=local_user_enabled,
            infrastructure_encryption_enabled=infrastructure_encryption_enabled,
            sftp_enabled=sftp_enabled,
            blob_properties=blob_properties,
            containers=containers,
            management_lock=management_lock,
        )


class StorageAccountL0(Construct):
    """
    A level 0 construct that creates and manages an Azure storage account.

    Attributes:
        storage_account (StorageAccount): The Azure storage account.
        management_lock (ManagementLockL0): The management lock applied to the storage account.
    """

    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        env: str,
        name: str,
        location: AzureLocation,
        sequence_number: str,
        account_replication_type: str,
        account_kind: str,
        account_tier: str,
        cross_tenant_replication_enabled: bool,
        access_tier: str,
        shared_access_key_enabled: bool,
        public_network_access_enabled: bool,
        is_hns_enabled: bool,
        local_user_enabled: bool,
        infrastructure_encryption_enabled: bool,
        sftp_enabled: bool,
        blob_properties: BlobProperties,
        containers: list[StorageContainerL0Config],
        management_lock: ManagementLockL0Config | None,
        resource_group_l0: ResourceGroupL0,
    ) -> None:
        """
        Initializes the StorageAccountL0 construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            name (str): The name of the storage account.
            location (AzureLocation): The Azure location.
            sequence_number (str): The sequence number.
            account_replication_type (str): The replication type of the storage account.
            account_kind (str): The kind of the storage account.
            account_tier (str): The tier of the storage account.
            cross_tenant_replication_enabled (bool): Whether cross-tenant replication is enabled.
            access_tier (str): The access tier of the storage account.
            shared_access_key_enabled (bool): Whether shared access key is enabled.
            public_network_access_enabled (bool): Whether public network access is enabled.
            is_hns_enabled (bool): Whether hierarchical namespace is enabled.
            local_user_enabled (bool): Whether local user is enabled.
            infrastructure_encryption_enabled (bool): Whether infrastructure encryption is enabled.
            sftp_enabled (bool): Whether SFTP is enabled.
            blob_properties (BlobProperties): The blob properties configuration.
            containers (list[StorageContainerL0Config]): The list of storage containers configuration.
            management_lock (ManagementLockL0Config | None): The management lock configuration.
            resource_group_l0 (ResourceGroupL0): The resource group level 0 construct.
        """
        super().__init__(scope, id_)

        self.full_name = f"{AzureResource.STORAGE_ACCOUNT.abbr}{env}{name}{location.name}{sequence_number}"
        self._resource_group_l0 = resource_group_l0
        self._storage_account = StorageAccount(
            self,
            f"StorageAccount_{self.full_name}",
            name=self.full_name,
            location=location.name,
            resource_group_name=self._resource_group_l0.resource_group.name,
            account_replication_type=account_replication_type,
            account_kind=account_kind,
            account_tier=account_tier,
            cross_tenant_replication_enabled=cross_tenant_replication_enabled,
            access_tier=access_tier,
            shared_access_key_enabled=shared_access_key_enabled,
            public_network_access_enabled=public_network_access_enabled,
            is_hns_enabled=is_hns_enabled,
            local_user_enabled=local_user_enabled,
            infrastructure_encryption_enabled=infrastructure_encryption_enabled,
            sftp_enabled=sftp_enabled,
            blob_properties=StorageAccountBlobProperties(
                delete_retention_policy=StorageAccountBlobPropertiesDeleteRetentionPolicy(
                    days=blob_properties.delete_retention_policy.days,
                )
            ),
        )

        for container in containers:
            StorageContainerL0.from_config(
                self,
                f"StorageContainerL0_{container.full_name}",
                env=env,
                config=container,
                storage_account_id=self.storage_account.id,
            )
        if management_lock:
            self._management_lock: ManagementLockL0 | None = ManagementLockL0.from_config(
                self,
                "ManagementLockL0",
                env=env,
                name=name,
                resource_id=self.storage_account.id,
                config=management_lock,
            )
        else:
            self._management_lock = None

    @property
    def full_name(self) -> str:
        """Gets the full name for the storage account."""
        return self._full_name

    @full_name.setter
    def full_name(self, value: str) -> None:
        """
        Sets the full name for the storage account.

        Args:
            value (str): The full name to set.
        """
        self._full_name = value

    @property
    def storage_account(self) -> StorageAccount:
        """Gets the Azure storage account."""
        return self._storage_account

    @property
    def management_lock(self) -> ManagementLockL0 | None:
        """Gets the management lock applied to the storage account."""
        return self._management_lock

    @classmethod
    def from_config(
        cls, scope: Construct, id_: str, env: str, config: StorageAccountL0Config, resource_group_l0: ResourceGroupL0
    ) -> Self:
        """
        Create a StorageAccountL0 instance from a StorageAccountL0Config object.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            config (StorageAccountL0Config): The configuration object for the storage account.
            resource_group_l0 (ResourceGroupL0): The resource group level 0 construct.

        Returns:
            StorageAccountL0: A fully-initialized StorageAccountL0 instance.
        """
        return cls(
            scope,
            id_,
            env=env,
            name=config.name,
            location=config.location,
            sequence_number=config.sequence_number,
            account_replication_type=config.account_replication_type,
            account_kind=config.account_kind,
            account_tier=config.account_tier,
            cross_tenant_replication_enabled=config.cross_tenant_replication_enabled,
            access_tier=config.access_tier,
            shared_access_key_enabled=config.shared_access_key_enabled,
            public_network_access_enabled=config.public_network_access_enabled,
            is_hns_enabled=config.is_hns_enabled,
            local_user_enabled=config.local_user_enabled,
            infrastructure_encryption_enabled=config.infrastructure_encryption_enabled,
            sftp_enabled=config.sftp_enabled,
            blob_properties=config.blob_properties,
            containers=config.containers,
            management_lock=config.management_lock,
            resource_group_l0=resource_group_l0,
        )
