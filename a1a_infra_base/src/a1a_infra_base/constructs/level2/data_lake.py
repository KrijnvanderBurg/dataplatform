"""
Module data_lake

This module defines the DataLakeL1 class, which creates multiple storage accounts
for a data lake following the medallion architecture pattern.

Classes:
    DataLakeL1: A construct that creates storage accounts for a data lake.
    DataLakeL1Config: A configuration class for DataLakeL1.
"""

import logging
from dataclasses import dataclass
from typing import Any, Final, Self

from a1a_infra_base.constructs.ABC import CombinedMeta, ConstructABC, ConstructConfigABC
from a1a_infra_base.constructs.level1.storage import StorageL1, StorageL1Config
from a1a_infra_base.logger import setup_logger
from constructs import Construct

logger: logging.Logger = setup_logger(__name__)

# Constants for dictionary keys
# root key
DATA_LAKE_KEY: Final[str] = "data_lake"
# attributes
SOURCE_STORAGE: Final[str] = "source_storage"
BRONZE_STORAGE: Final[str] = "bronze_storage"
SILVER_STORAGE: Final[str] = "silver_storage"
GOLD_STORAGE: Final[str] = "gold_storage"


@dataclass
class DataLakeL2Config(ConstructConfigABC):
    """
    A configuration class for DataLakeL1.

    Attributes:
        source_storage_l1_config (StorageL1Config): The configuration for the source storage account.
        bronze_storage_l1_config (StorageL1Config): The configuration for the bronze storage account.
        silver_storage_l1_config (StorageL1Config): The configuration for the silver storage account.
        gold_storage_l1_config (StorageL1Config): The configuration for the gold storage account.
    """

    source_storage_l1_config: StorageL1Config
    bronze_storage_l1_config: StorageL1Config
    silver_storage_l1_config: StorageL1Config
    gold_storage_l1_config: StorageL1Config

    @classmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        """
        Create a DataLakeL1Config by unpacking parameters from a configuration dictionary.

        Args:
            dict_ (dict): A dictionary containing the configuration.

        Returns:
            DataLakeL1Config: A fully-initialized DataLakeL1Config.
        """

        # I can use a dataclass replace function and supply the dict, this works great except the from_dict is never actually called then.
        # So any processing that is required to initialise the object isnt done, this is most notable in the location attribute.
        # I create an enum based on the string which is the location attribute, therefore location attribute is an enum. But when using
        # replace with dataclass its initialised based on dict, so the location attribute is a string and never properly processed.
        # the program will then crash later on calling the abbr getter I have added to the enum.

        source_storage_l1_config = StorageL1Config.from_dict(dict_[SOURCE_STORAGE])
        bronze_storage_l1_config = StorageL1Config.from_dict(dict_[SOURCE_STORAGE])
        silver_storage_l1_config = StorageL1Config.from_dict(dict_[SOURCE_STORAGE])
        gold_storage_l1_config = StorageL1Config.from_dict(dict_[SOURCE_STORAGE])

        return cls(
            source_storage_l1_config=source_storage_l1_config,
            bronze_storage_l1_config=bronze_storage_l1_config,
            silver_storage_l1_config=silver_storage_l1_config,
            gold_storage_l1_config=gold_storage_l1_config,
        )


class DataLakeL2(Construct, ConstructABC, metaclass=CombinedMeta):
    """
    A level 1 construct that creates and manages multiple storage accounts
    following the medallion architecture pattern (source, bronze, silver, gold).

    Attributes:
        source_storage_l1 (StorageL1): The source storage account.
        bronze_storage_l1 (StorageL1): The bronze storage account.
        silver_storage_l1 (StorageL1): The silver storage account.
        gold_storage_l1 (StorageL1): The gold storage account.
    """

    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        env: str,
        config: DataLakeL2Config,
        resource_group_name: str,
    ) -> None:
        """
        Initializes the DataLakeL1 construct.

        Args:
            scope (Construct): The scope in which this construct is defined.
            id_ (str): The scoped construct ID.
            env (str): The environment name.
            config (DataLakeL1Config): The configuration for the data lake.
            resource_group_name (str): The name of the resource group to create the storage accounts in.
        """
        super().__init__(scope, id_)

        self._source_storage_l1 = StorageL1(
            self,
            "StorageL1_Source",
            env=env,
            config=config.source_storage_l1_config,
            resource_group_name=resource_group_name,
        )

        self._bronze_storage_l1 = StorageL1(
            self,
            "StorageL1_Bronze",
            env=env,
            config=config.bronze_storage_l1_config,
            resource_group_name=resource_group_name,
        )

        self._silver_storage_l1 = StorageL1(
            self,
            "StorageL1_Silver",
            env=env,
            config=config.silver_storage_l1_config,
            resource_group_name=resource_group_name,
        )

        self._gold_storage_l1 = StorageL1(
            self,
            "StorageL1_Gold",
            env=env,
            config=config.gold_storage_l1_config,
            resource_group_name=resource_group_name,
        )

    @property
    def source_storage_l1(self) -> StorageL1:
        return self._source_storage_l1

    @property
    def bronze_storage_l1(self) -> StorageL1:
        return self._bronze_storage_l1

    @property
    def silver_storage_l1(self) -> StorageL1:
        return self._silver_storage_l1

    @property
    def gold_storage_l1(self) -> StorageL1:
        return self._gold_storage_l1
