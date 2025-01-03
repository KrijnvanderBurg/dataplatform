"""
Module storage_account

This module defines the StorageAccountL0 class, which is responsible for creating
and managing an Azure storage account with specific configurations.

Classes:
    StorageAccountL0: A level 0 construct that creates and manages an Azure storage account.
"""

from cdktf_cdktf_provider_azurerm.storage_account import (
    StorageAccount,
    StorageAccountBlobProperties,
    StorageAccountBlobPropertiesDeleteRetentionPolicy,
)
from constructs import Construct
from a1a_infra_base.constants import AzureLocation, AzureResource
from a1a_infra_base.constructs.level0.resource_group import ResourceGroupL0


class StorageAccountL0(Construct):
    """
    A level 0 construct that creates and manages an Azure storage account.

    Attributes:
        storage_account (StorageAccount): The Azure storage account.
    """

    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        name: str,
        env: str,
        location: AzureLocation,
        sequence_number: str,
        resource_group_l0: ResourceGroupL0,
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
        delete_retention_days: int,
    ) -> None:
        """
        Initializes the StorageAccountL0 construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            name (str): The name of the storage account.
            env (str): The environment name.
            location (AzureLocation): The Azure location.
            sequence_number (str): The sequence number.
            resource_group_l0 (ResourceGroupL0): The resource group level 0 construct.
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
            delete_retention_days (int): The number of days to retain deleted items.
        """
        super().__init__(scope, id_)
        self._storage_account = StorageAccount(
            self,
            f"{AzureResource.STORAGE_ACCOUNT.abbr}_{name}_{env}_{location.abbr}_{sequence_number}",
            name=f"{AzureResource.STORAGE_ACCOUNT.abbr}-{name}-{env}-{location.abbr}-{sequence_number}",
            location=location.name,
            resource_group_name=resource_group_l0.resource_group.name,
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
                    days=delete_retention_days,
                )
            ),
        )

    @property
    def storage_account(self) -> StorageAccount:
        """Gets the Azure storage account."""
        return self._storage_account
