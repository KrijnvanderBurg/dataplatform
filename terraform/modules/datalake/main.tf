resource "azurerm_storage_account" "data_lake" {
  name                     = "st${var.storage_account_name}${var.environment}${var.location_primary_abbr}${var.sequence_number}"
  resource_group_name      = var.resource_group_name
  location                 = var.location_primary
  account_tier             = "Standard"
  account_replication_type = var.account_replication_type

  lifecycle {
    prevent_destroy = true
  }
}

resource "azurerm_management_lock" "source_lock" {
  name       = "${azurerm_storage_account.data_lake.name}-lock"
  scope      = azurerm_storage_account.data_lake.id
  lock_level = "CanNotDelete"
}

resource "azurerm_storage_container" "container" {
  for_each              = var.containers
  name                  = each.value
  storage_account_id    = azurerm_storage_account.data_lake.id
  container_access_type = "private"

  lifecycle {
    prevent_destroy = true
  }
}