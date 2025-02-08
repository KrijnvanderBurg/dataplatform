resource "azurerm_resource_group" "remote_backend" {
  name     = "rg-tfbackend-${var.environment}-${var.location_primary_abbr}-01"
  location = var.location_primary
}

resource "azurerm_management_lock" "remote_backend_lock" {
  name       = "${azurerm_resource_group.remote_backend.name}-lock"
  scope      = azurerm_resource_group.remote_backend.id
  lock_level = "CanNotDelete"
}

resource "azurerm_storage_account" "remote_backend" {
  name                     = "sttfbackend${var.environment}${var.location_primary_abbr}01"
  resource_group_name      = azurerm_resource_group.remote_backend.name
  location                 = var.location_primary
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_management_lock" "storage_account_lock" {
  name       = "${azurerm_storage_account.remote_backend.name}-lock"
  scope      = azurerm_storage_account.remote_backend.id
  lock_level = "CanNotDelete"
}

resource "azurerm_storage_container" "backend" {
  name                  = "tfstate"
  storage_account_id    = azurerm_storage_account.remote_backend.id
  container_access_type = "private"
}
