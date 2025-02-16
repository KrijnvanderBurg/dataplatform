output "databricks_workspace_id" {
  value = azurerm_databricks_workspace.this.id
}

output "vnet_id" {
  value = azurerm_virtual_network.vnet.id
}

output "private_endpoint_id" {
  value = azurerm_private_endpoint.databricks_pe.id
}
