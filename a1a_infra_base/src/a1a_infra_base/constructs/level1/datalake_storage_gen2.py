# """
# Module datalake_l1

# Defines a DatalakeL1 construct using just the StorageAccountL0.
# """

# import logging
# from dataclasses import dataclass

# from constructs import Construct

# from a1a_infra_base.constructs.level0.storage_account import StorageAccountL0, StorageAccountL0Config
# from a1a_infra_base.constructs.level0.resource_group import ResourceGroupL0

# logger = logging.getLogger(__name__)


# @dataclass
# class DatalakeL1Config:
#     """
#     Configuration for DatalakeL1.

#     Attributes:
#         env (str): Environment identifier.
#         storage_account_config (StorageAccountL0Config): Storage account config.
#     """

#     env: str
#     storage_account_config: StorageAccountL0Config


# class DatalakeL1(Construct):
#     """
#     A level1 construct that only composes StorageAccountL0 for a data lake.
#     """

#     def __init__(
#         self, scope: Construct, id_: str, *, config: DatalakeL1Config, resource_group_l0: ResourceGroupL0
#     ) -> None:
#         super().__init__(scope, id_)
#         self._storage_account_l0 = StorageAccountL0(
#             self,
#             f"sa_{config.env}",
#             config=config.storage_account_config,
#             resource_group_l0=resource_group_l0,
#         )

#     @property
#     def storage_account_l0(self) -> StorageAccountL0:
#         """Returns the underlying StorageAccountL0."""
#         return self._storage_account_l0
