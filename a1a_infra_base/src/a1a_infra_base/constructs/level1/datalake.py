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

from a1a_infra_base.constructs.construct_abc import CombinedMeta, ConstructConfigABC
from a1a_infra_base.constructs.level0.storage_account import StorageAccountL0, StorageAccountL0Config
from a1a_infra_base.logger import setup_logger
from constructs import Construct

logger: logging.Logger = setup_logger(__name__)


@dataclass
class DataLakeL1Config(StorageAccountL0Config, ConstructConfigABC):
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

    is_hns_enabled: bool | None = True


class DataLakeL1(StorageAccountL0, Construct, metaclass=CombinedMeta):
    """
    A level 0 construct that creates and manages an Azure storage account.

    Attributes:
        storage_account (StorageAccount): The Azure storage account.
        management_lock (ManagementLockL0): The management lock applied to the storage account.
    """
