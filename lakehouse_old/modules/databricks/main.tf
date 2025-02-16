resource "azurerm_virtual_network" "vnet" {
  name                = var.vnet_name
  resource_group_name = var.resource_group_name
  location            = var.location
  address_space       = var.vnet_address_space
}

resource "azurerm_subnet" "databricks_subnet" {
  name                 = var.subnet_name
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = var.subnet_address_prefix
  delegation {
    name = "databricks_delegation"
    service_delegation {
      name = "Microsoft.Databricks/workspaces"
      actions = ["Microsoft.Network/virtualNetworks/subnets/join/action"]
    }
  }
}

resource "azurerm_databricks_workspace" "this" {
  name                = var.databricks_workspace_name
  resource_group_name = var.resource_group_name
  location            = var.location
  sku                 = "standard"
  managed_resource_group_id = "${var.resource_group_name}-databricks-rg"
  
  custom_parameters {
    no_public_ip = true
    virtual_network_id = azurerm_virtual_network.vnet.id
    public_subnet_name = ""  # Not used due to VNET injection
    private_subnet_name = azurerm_subnet.databricks_subnet.name
  }
}

resource "azurerm_private_endpoint" "databricks" {
  name                = var.private_endpoint_name
  location            = var.location
  resource_group_name = var.resource_group_name
  subnet_id           = azurerm_subnet.databricks_subnet.id

  private_service_connection {
    name                           = "databricksConnection"
    private_connection_resource_id = azurerm_databricks_workspace.this.id
    is_manual_connection           = false
    subresource_names              = ["databricks_ui_endpoint"]
  }
}
