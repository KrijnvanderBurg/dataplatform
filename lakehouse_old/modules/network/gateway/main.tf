resource "azurerm_subnet" "gateway_subnet" {
  name                 = "subnet-gateway-${var.environment}"
  resource_group_name  = data.azurerm_virtual_network.vnet.resource_group_name
  virtual_network_name = data.azurerm_virtual_network.vnet.name
  address_prefixes     = var.gateway_subnet_address_prefix
}

resource "azurerm_public_ip" "vpn_gateway_ip" {
  name                = "pip-vpn-${var.environment}"
  location            = data.azurerm_virtual_network.vnet.location
  resource_group_name = data.azurerm_virtual_network.vnet.resource_group_name
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_virtual_network_gateway" "vpn_gateway" {
  name                = "vgw-vpn-${var.environment}"
  location            = data.azurerm_virtual_network.vnet.location
  resource_group_name = data.azurerm_virtual_network.vnet.resource_group_name
  type                = "Vpn"
  vpn_type            = "RouteBased"
  active_active       = false
  sku                 = "VpnGw1"
  ip_configuration {
    name                = "vnetGatewayConfig"
    public_ip_address_id = azurerm_public_ip.vpn_gateway_ip.id
    subnet_id           = azurerm_subnet.gateway_subnet.id
  }
}

resource "azurerm_local_network_gateway" "onprem_gateway" {
  name                = "lgw-onprem-${var.environment}"
  location            = data.azurerm_virtual_network.vnet.location
  resource_group_name = data.azurerm_virtual_network.vnet.resource_group_name
  gateway_address     = var.onprem_vpn_gateway_ip
  address_space       = var.onprem_address_space
}

resource "azurerm_virtual_network_gateway_connection" "connection" {
  name                       = "con-vnet2onprem-${var.environment}"
  location                   = data.azurerm_virtual_network.vnet.location
  resource_group_name        = data.azurerm_virtual_network.vnet.resource_group_name
  type                       = "IPsec"
  virtual_network_gateway_id = azurerm_virtual_network_gateway.vpn_gateway.id
  local_network_gateway_id   = azurerm_local_network_gateway.onprem_gateway.id
  connection_protocol        = "IKEv2"
  shared_key                 = var.vpn_shared_key
}
