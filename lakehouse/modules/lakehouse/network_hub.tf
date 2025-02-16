// hub
resource "azurerm_virtual_network" "hub" {
  name                = "vnet-hub-${var.location_short}"
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
  address_space       = [var.vnet_hub_cidr]
  tags                = local.tags
}

resource "azurerm_subnet" "hubfw" {
  //name must be fixed as AzureFirewallSubnet
  name                 = "AzureFirewallSubnet"
  resource_group_name  = azurerm_resource_group.this.name
  virtual_network_name = azurerm_virtual_network.hub.name
  address_prefixes     = [cidrsubnet(var.vnet_hub_cidr, 8, 0)] // cidr/16 + /8 = /24 = 256 addresses
}

// firewall
resource "azurerm_public_ip" "fwpublicip" {
  name                = "pip-afwhub"
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_firewall" "hubfw" {
  name                = "afw-hub"
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
  sku_name            = "AZFW_VNet"
  sku_tier            = "Standard"

  ip_configuration {
    name                 = "configuration"
    subnet_id            = azurerm_subnet.hubfw.id
    public_ip_address_id = azurerm_public_ip.fwpublicip.id
  }
}
