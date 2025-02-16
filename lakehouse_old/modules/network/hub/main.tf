resource "azurerm_virtual_network" "hub" {
  name                = var.vnet_name
  resource_group_name = var.resource_group_name
  location            = var.location
  address_space       = var.hub_vnet_address_space
}

# resource "azurerm_network_security_group" "hub_nsg" {
#   name                = "${var.hub_name}-nsg"
#   location            = var.location
#   resource_group_name = var.resource_group_name

#   security_rule {
#     name                       = "AllowFromGatewaySubnet"
#     priority                   = 100
#     direction                  = "Inbound"
#     access                     = "Allow"
#     protocol                   = "*"
#     source_address_prefix      = "10.2.0.0/24"
#     destination_address_prefix = "*"
#     destination_port_range     = "*"
#   }
# }
