# # Minimal example illustrating how to build all the required resources in a single CDKTF stack,
# # reusing the existing L0 ResourceGroup classes. Only essential fields are specified.

# from dataclasses import dataclass
# from typing import Any, Self

# from cdktf import TerraformStack
# from cdktf_cdktf_provider_azurerm.bastion_host import BastionHost
# from cdktf_cdktf_provider_azurerm.databricks_workspace import DatabricksWorkspace
# from cdktf_cdktf_provider_azurerm.firewall import Firewall
# from cdktf_cdktf_provider_azurerm.network_security_group import NetworkSecurityGroup
# from cdktf_cdktf_provider_azurerm.private_dns_zone import PrivateDnsZone
# from cdktf_cdktf_provider_azurerm.purview_account import PurviewAccount

# # Import azurerm constructs directly for resources where no L0 component exists yet
# from cdktf_cdktf_provider_azurerm.virtual_network import VirtualNetwork
# from cdktf_cdktf_provider_azurerm.vpn_gateway import VpnGateway
# from cdktf_cdktf_provider_azurerm.vpn_gateway_connection import VpnGatewayConnection
# from constructs import Construct

# # Reuse existing L0 constructs
# from a1a_infra_base.constructs.level0.resource_group import ResourceGroupL0, ResourceGroupL0Config
# from a1a_infra_base.constructs.level0.storage_account import StorageAccountL0, StorageAccountL0Config


# @dataclass
# class LakehouseStackConfig:
#     """
#     Holds config for each resource group plus optional instructions for resources within them.
#     Only the minimal fields are shown here. You can expand them as needed.
#     """

#     env: str
#     core_networking_rg: dict[str, Any]
#     process_rg: dict[str, Any]
#     storage_rg: dict[str, Any]
#     user_access_rg: dict[str, Any]
#     # Example: Provide storage account config if needed
#     storage_account_config: dict[str, Any] | None = None

#     @classmethod
#     def from_config(cls, env: str, config: dict[str, Any]) -> Self:
#         return cls(
#             env=env,
#             core_networking_rg=config["core_networking_rg"],
#             process_rg=config["process_rg"],
#             storage_rg=config["storage_rg"],
#             user_access_rg=config["user_access_rg"],
#             storage_account_config=config.get("storage_account_config"),
#         )


# class LakehouseStack(TerraformStack):
#     def __init__(self, scope: Construct, id_: str, *, config: LakehouseStackConfig) -> None:
#         super().__init__(scope, id_)

#         # =================================================================================
#         # CORE NETWORKING RG
#         # =================================================================================
#         self._core_networking_rg_l0 = ResourceGroupL0(
#             self,
#             "CoreNetworkingRG",
#             config=ResourceGroupL0Config.from_dict(env=config.env, config=config.core_networking_rg),
#         )
#         core_rg_name = self._core_networking_rg_l0.resource_group.name
#         core_rg_loc = self._core_networking_rg_l0.resource_group.location

#         # Minimal Hub VNet
#         self._core_vnet = VirtualNetwork(
#             self,
#             "HubVNet",
#             name="hub-vnet",
#             resource_group_name=core_rg_name,
#             location=core_rg_loc,
#             address_space=["10.0.0.0/16"],
#         )

#         # Azure Firewall
#         # (Usually also needs a firewall subnet, etc., omitted for brevity.)
#         self._azure_firewall = Firewall(
#             self,
#             "CoreFirewall",
#             name="core-firewall",
#             resource_group_name=core_rg_name,
#             location=core_rg_loc,
#             sku_name="AZFW_VNet",
#         )

#         # VPN Gateway
#         # (Requires a gateway subnet + public IP, omitted here for brevity.)
#         self._vpn_gateway = VpnGateway(
#             self,
#             "CoreVpnGateway",
#             name="core-vpngw",
#             location=core_rg_loc,
#             resource_group_name=core_rg_name,
#             virtual_network_id=self._core_vnet.id,
#         )
#         # Minimal connection (typically you need local_network_gateway, etc.)
#         self._vpn_conn = VpnGatewayConnection(
#             self,
#             "CoreVpnGatewayConn",
#             name="core-vpnconn",
#             resource_group_name=core_rg_name,
#             vpn_gateway_id=self._vpn_gateway.id,
#             connection_protocol="IKEv2",
#             connection_type="ExpressRoute",  # or "IPsec"
#             routing_weight=10,
#         )

#         # Private DNS Zone
#         self._private_dns_zone = PrivateDnsZone(
#             self,
#             "CorePrivDns",
#             name="privatelink.local",
#             resource_group_name=core_rg_name,
#         )

#         # Core NSG
#         self._core_nsg = NetworkSecurityGroup(
#             self,
#             "CoreNSG",
#             name="core-nsg",
#             resource_group_name=core_rg_name,
#             location=core_rg_loc,
#         )

#         # =================================================================================
#         # PROCESS RG
#         # =================================================================================
#         self._process_rg_l0 = ResourceGroupL0(
#             self,
#             "ProcessRG",
#             config=ResourceGroupL0Config.from_dict(env=config.env, config=config.process_rg),
#         )
#         process_rg_name = self._process_rg_l0.resource_group.name
#         process_rg_loc = self._process_rg_l0.resource_group.location

#         # Spoke VNet (Process)
#         self._process_vnet = VirtualNetwork(
#             self,
#             "ProcessVNet",
#             name="process-vnet",
#             resource_group_name=process_rg_name,
#             location=process_rg_loc,
#             address_space=["10.1.0.0/16"],
#         )

#         # Minimal Databricks Workspace
#         # (Typically also needs more fields, e.g. Managed Resource Group. Omitted for brevity.)
#         self._databricks_ws = DatabricksWorkspace(
#             self,
#             "DatabricksWorkspace",
#             name="process-dbw",
#             resource_group_name=process_rg_name,
#             location=process_rg_loc,
#             sku="premium",
#         )

#         # Minimal Databricks Cluster
#         self._databricks_cluster = DatabricksCluster(
#             self,
#             "DatabricksCluster",
#             name="db-cluster",
#             workspace_id=self._databricks_ws.id,
#             cluster_version="13.0.x-scala2.12",  # example version
#             node_type_id="Standard_DS3_v2",
#             num_workers=2,
#         )

#         # Azure Purview
#         # Typically must specify account tier, scanning region, etc. Minimal mandatory fields:
#         self._purview = PurviewAccount(
#             self,
#             "PurviewAccount",
#             name="process-purview",
#             resource_group_name=process_rg_name,
#             location=process_rg_loc,
#             sku_name="Standard",
#         )

#         # NSG for Process RG
#         self._process_nsg = NetworkSecurityGroup(
#             self,
#             "ProcessNSG",
#             name="process-nsg",
#             resource_group_name=process_rg_name,
#             location=process_rg_loc,
#         )

#         # =================================================================================
#         # STORAGE RG
#         # =================================================================================
#         self._storage_rg_l0 = ResourceGroupL0(
#             self,
#             "StorageRG",
#             config=ResourceGroupL0Config.from_dict(env=config.env, config=config.storage_rg),
#         )
#         storage_rg_name = self._storage_rg_l0.resource_group.name
#         storage_rg_loc = self._storage_rg_l0.resource_group.location

#         # Optionally create a Storage Account via L0
#         # (We can add more containers or lock configs as needed.)
#         if config.storage_account_config:
#             self._storage_account_l0 = StorageAccountL0(
#                 self,
#                 "StorageL0",
#                 config=StorageAccountL0Config.from_dict(env=config.env, config=config.storage_account_config),
#                 resource_group_l0=self._storage_rg_l0,
#             )

#         # Spoke VNet (Storage)
#         self._storage_vnet = VirtualNetwork(
#             self,
#             "StorageVNet",
#             name="storage-vnet",
#             resource_group_name=storage_rg_name,
#             location=storage_rg_loc,
#             address_space=["10.2.0.0/16"],
#         )

#         # NSG for Storage RG
#         self._storage_nsg = NetworkSecurityGroup(
#             self,
#             "StorageNSG",
#             name="storage-nsg",
#             resource_group_name=storage_rg_name,
#             location=storage_rg_loc,
#         )

#         # =================================================================================
#         # USER ACCESS RG
#         # =================================================================================
#         self._user_access_rg_l0 = ResourceGroupL0(
#             self,
#             "UserAccessRG",
#             config=ResourceGroupL0Config.from_dict(env=config.env, config=config.user_access_rg),
#         )
#         user_access_rg_name = self._user_access_rg_l0.resource_group.name
#         user_access_rg_loc = self._user_access_rg_l0.resource_group.location

#         # Spoke VNet (User Access)
#         self._user_vnet = VirtualNetwork(
#             self,
#             "UserAccessVNet",
#             name="user-access-vnet",
#             resource_group_name=user_access_rg_name,
#             location=user_access_rg_loc,
#             address_space=["10.3.0.0/16"],
#         )

#         # Azure Bastion
#         # (Usually must add a Bastion subnet. Omitted.)
#         self._bastion = BastionHost(
#             self,
#             "UserBastion",
#             name="user-bastion",
#             resource_group_name=user_access_rg_name,
#             location=user_access_rg_loc,
#             # minimal config, typically you need a public IP
#             ip_configuration=[
#                 {
#                     "name": "bastion-ip-config",
#                     "subnet_id": "${azurerm_subnet.user-bastion-subnet.id}",  # placeholder
#                     "public_ip_address_id": "placeholder-pip-id",
#                 }
#             ],
#         )

#         # Another VPN Gateway for user RG if needed
#         self._user_vpn_gateway = VpnGateway(
#             self,
#             "UserVpnGateway",
#             name="user-vpngw",
#             location=user_access_rg_loc,
#             resource_group_name=user_access_rg_name,
#             virtual_network_id=self._user_vnet.id,
#         )

#         # NSG for User Access RG
#         self._user_nsg = NetworkSecurityGroup(
#             self,
#             "UserNSG",
#             name="user-nsg",
#             resource_group_name=user_access_rg_name,
#             location=user_access_rg_loc,
#         )
