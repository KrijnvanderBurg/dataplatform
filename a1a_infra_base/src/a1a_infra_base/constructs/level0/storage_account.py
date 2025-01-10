"""
Module storage_account

This module defines the StorageAccountL0 class and the StorageAccountL0Config class,
which are responsible for creating and managing an Azure storage account with specific configurations.

Classes:
    StorageAccountL0: A level 0 construct that creates and manages an Azure storage account.
    StorageAccountL0Config: A configuration class for StorageAccountL0.
"""

import logging
from dataclasses import dataclass
from typing import Any, Final, Self

from cdktf_cdktf_provider_azurerm.storage_account import (
    StorageAccount,
    StorageAccountBlobProperties,
    StorageAccountBlobPropertiesDeleteRetentionPolicy,
)

from a1a_infra_base.constants import AzureLocation, AzureResource
from a1a_infra_base.constructs.construct_abc import CombinedMeta, ConstructConfigABC
from a1a_infra_base.constructs.level0.management_lock import ManagementLockL0, ManagementLockL0Config
from a1a_infra_base.constructs.level0.storage_container import StorageContainerL0, StorageContainerL0Config
from a1a_infra_base.logger import setup_logger
from constructs import Construct

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
BLOB_PROPERTIES_L0_KEY: Final[str] = "blob_properties_l0"
DELETE_RETENTION_POLICY_L0_KEY: Final[str] = "delete_retention_policy_l0"
DAYS_KEY: Final[str] = "days"
STORAGE_CONTAINERS_L0_KEY: Final[str] = "storage_containers_l0"
MANAGEMENT_LOCK_L0_KEY: Final[str] = "management_lock_l0"


@dataclass
class DeleteRetentionPolicyL0Config:
    """
    A class to represent the delete retention policy configuration.

    Attributes:
        days (int): The number of days to retain deleted items.
    """

    days: int | None = None

    @classmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Create a DeleteRetentionPolicy by unpacking parameters from a configuration dictionary.

        Args:
            dict_ (dict): A dictionary containing delete retention policy configuration.

        Returns:
            DeleteRetentionPolicy: A fully-initialized DeleteRetentionPolicy.
        """
        days = dict_.get(DAYS_KEY, cls.days)
        return cls(days=days)


@dataclass
class BlobPropertiesL0Config:
    """
    A class to represent the blob properties configuration.

    Attributes:
        delete_retention_policy (DeleteRetentionPolicy): The delete retention policy configuration.
    """

    delete_retention_policy_l0: DeleteRetentionPolicyL0Config | None = None

    @classmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Create a BlobProperties by unpacking parameters from a configuration dictionary.

        Args:
            dict_ (dict): A dictionary containing blob properties configuration.

        Returns:
            BlobProperties: A fully-initialized BlobProperties.
        """

        delete_retention_policy_l0 = (
            DeleteRetentionPolicyL0Config.from_dict(dict_[DELETE_RETENTION_POLICY_L0_KEY])
            if DELETE_RETENTION_POLICY_L0_KEY in dict_
            else cls.delete_retention_policy_l0
        )

        return cls(delete_retention_policy_l0=delete_retention_policy_l0)


@dataclass
class StorageAccountL0Config(ConstructConfigABC):
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

    # custom added
    sequence_number: str
    # all StorageAccount parameters
    account_replication_type: str
    account_tier: str
    location: AzureLocation
    name: str
    access_tier: str | None = None
    account_kind: str | None = None
    # allowed_copy_scope: str | None = None
    # allow_nested_items_to_be_public: bool | None = None
    # azure_files_authentication: "StorageAccountAzureFilesAuthentication" | dict[str, any] | None = None
    blob_properties_l0: BlobPropertiesL0Config | None = None
    cross_tenant_replication_enabled: bool | None = False
    # custom_domain: "StorageAccountCustomDomain" | dict[str, any] | None = None
    # customer_managed_key: "StorageAccountCustomerManagedKey" | dict[str, any] | None = None
    # default_to_oauth_authentication: bool | None = None
    # dns_endpoint_type: str | None = None
    # edge_zone: str | None = None
    # https_traffic_only_enabled: bool | None = None
    id_: str | None = None
    # identity: "StorageAccountIdentity" | dict[str, any] | None = None
    # immutability_policy: "StorageAccountImmutabilityPolicy" | dict[str, any] | None = None
    infrastructure_encryption_enabled: bool | None = True
    is_hns_enabled: bool | None = None
    # large_file_share_enabled: bool | None = None
    local_user_enabled: bool | None = False
    min_tls_version: str | None = None
    # network_rules: "StorageAccountNetworkRules" | dict[str, any] | None = None
    nfsv3_enabled: bool | None = False
    public_network_access_enabled: bool | None = False
    # queue_encryption_key_type: str | None = None
    # queue_properties: "StorageAccountQueueProperties" | dict[str, any] | None = None
    # routing: "StorageAccountRouting" | dict[str, any] | None = None
    # sas_policy: "StorageAccountSasPolicy" | dict[str, any] | None = None
    sftp_enabled: bool | None = False
    shared_access_key_enabled: bool | None = False
    # share_properties: "StorageAccountShareProperties" | dict[str, any] | None = None
    # static_website: "StorageAccountStaticWebsite" | dict[str, any] | None = None
    # table_encryption_key_type: str | None = None
    tags: dict[str, str] | None = None
    # custom added
    storage_containers_l0: list[StorageContainerL0Config] | None = None
    management_lock_l0: ManagementLockL0Config | None = None

    @classmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Create a StorageAccountL0Config by unpacking parameters from a configuration dictionary.

        Expected format of 'dict_':
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
                    "name": "<container name>"
                }
            ],
            "management_lock": {
                "lock_level": "<lock level>",
                "notes": "<notes>"
            }
        }

        Args:
            dict_ (dict[str, Any]): A dictionary containing storage account configuration.

        Returns:
            StorageAccountL0Config: A fully-initialized StorageAccountL0Config.
        """
        name = dict_[NAME_KEY]
        location = AzureLocation.from_full_name(dict_[LOCATION_KEY])
        sequence_number = dict_[SEQUENCE_NUMBER_KEY]
        account_replication_type = dict_[ACCOUNT_REPLICATION_TYPE_KEY]
        account_kind = dict_.get(ACCOUNT_KIND_KEY, cls.account_kind)
        account_tier = dict_[ACCOUNT_TIER_KEY]
        cross_tenant_replication_enabled = dict_.get(
            CROSS_TENANT_REPLICATION_ENABLED_KEY, cls.cross_tenant_replication_enabled
        )
        access_tier = dict_.get(ACCESS_TIER_KEY, cls.access_tier)
        shared_access_key_enabled = dict_.get(SHARED_ACCESS_KEY_ENABLED_KEY, cls.shared_access_key_enabled)
        public_network_access_enabled = dict_.get(PUBLIC_NETWORK_ACCESS_ENABLED_KEY, cls.public_network_access_enabled)
        is_hns_enabled = dict_.get(IS_HNS_ENABLED_KEY, cls.is_hns_enabled)
        local_user_enabled = dict_.get(LOCAL_USER_ENABLED_KEY, cls.local_user_enabled)
        infrastructure_encryption_enabled = dict_.get(
            INFRASTRUCTURE_ENCRYPTION_ENABLED_KEY, cls.infrastructure_encryption_enabled
        )
        sftp_enabled = dict_.get(SFTP_ENABLED_KEY, cls.sftp_enabled)

        blob_properties_l0 = (
            BlobPropertiesL0Config.from_dict(dict_[BLOB_PROPERTIES_L0_KEY])
            if BLOB_PROPERTIES_L0_KEY in dict_
            else cls.blob_properties_l0
        )

        storage_containers_l0 = []
        container_dicts = dict_.get(STORAGE_CONTAINERS_L0_KEY, [])
        for container_dict in container_dicts:
            storage_containers_l0.append(StorageContainerL0Config.from_dict(dict_=container_dict))

        management_lock_l0 = (
            ManagementLockL0Config.from_dict(dict_[MANAGEMENT_LOCK_L0_KEY])
            if MANAGEMENT_LOCK_L0_KEY in dict_
            else cls.management_lock_l0
        )

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
            blob_properties_l0=blob_properties_l0,
            storage_containers_l0=storage_containers_l0,
            management_lock_l0=management_lock_l0,
        )


class StorageAccountL0(Construct, metaclass=CombinedMeta):
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
        config: StorageAccountL0Config,
        resource_group_name: str,
    ) -> None:
        """
        Initializes the StorageAccountL0 construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            config (StorageAccountL0Config): The configuration for the storage account.
            resource_group_name (str): The name of the resource group.
        """
        super().__init__(scope, id_)

        self.full_name = (
            f"{AzureResource.STORAGE_ACCOUNT.abbr}{config.name}{env}{config.location.abbr}{config.sequence_number}"
        )

        blob_properties = None
        if config.blob_properties_l0 is not None:
            delete_retention_policy = None
            if config.blob_properties_l0.delete_retention_policy_l0 is not None:
                delete_retention_policy = StorageAccountBlobPropertiesDeleteRetentionPolicy(
                    days=config.blob_properties_l0.delete_retention_policy_l0.days
                )

            blob_properties = StorageAccountBlobProperties(delete_retention_policy=delete_retention_policy)

        self._storage_account = StorageAccount(
            self,
            f"StorageAccount_{self.full_name}",
            name=self.full_name,
            location=config.location.full_name,
            resource_group_name=resource_group_name,
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
            blob_properties=blob_properties,
        )

        if config.storage_containers_l0 is not None:
            for container in config.storage_containers_l0:  # type: ignore
                StorageContainerL0(
                    self,
                    f"StorageContainerL0_{container.name}",
                    _=env,
                    config=container,
                    storage_account_id=self.storage_account.id,
                )

        if config.management_lock_l0:
            self._management_lock: ManagementLockL0 | None = ManagementLockL0(
                self,
                "ManagementLockL0",
                _=env,
                config=config.management_lock_l0,
                resource_id=self.storage_account.id,
                resource_name=self.full_name,
            )
        else:
            self._management_lock = None

    @property
    def storage_account(self) -> StorageAccount:
        """Gets the Azure storage account."""
        return self._storage_account
