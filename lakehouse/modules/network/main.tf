module "hub" {
  source = "/hub"
  location = var.location
  resource_group_name = var.resource_group_name
  net_name = var.hub_vnet_name
  vnet_address_space = var.hub_vnet_address_space
}

module "spoke_gateway" {
  source = "/spoke"
  location = var.location
  resource_group_name = var.resource_group_name
  vnet_name = var.spoke_vnet_name
  vnet_address_space = var.spoke_vnet_address_space
  hub_vnet_id = module.hub.vnet_id
}