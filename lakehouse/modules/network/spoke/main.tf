resource "azurerm_virtual_network" "spoke" {
  name                = var.vnet_name
  resource_group_name = var.resource_group_name
  location            = var.location
  address_space       = var.vnet_address_space
}

resource "azurerm_virtual_network_peering" "hub_to_spoke" {
  name                      = "peer-${azurerm_virtual_network.spoke.name}2${azurerm_virtual_network.spoke.name}-${var.environment}-${var.sequence_number}"
  resource_group_name       = var.resource_group_name
  virtual_network_name      = azurerm_virtual_network.spoke.name
  remote_virtual_network_id = var.hub_vnet_id

  allow_forwarded_traffic      = true
  allow_virtual_network_access = true
}
