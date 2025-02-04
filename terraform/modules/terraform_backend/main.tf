resource "azurerm_resource_group" "backend" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_management_lock" "resource_group_lock" {
  name       = "resource-group-lock"
  scope      = azurerm_resource_group.backend.id
  lock_level = "CanNotDelete"
}

resource "azurerm_storage_account" "backend" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.backend.name
  location                 = azurerm_resource_group.backend.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_management_lock" "storage_account_lock" {
  name       = "storage-account-lock"
  scope      = azurerm_storage_account.backend.id
  lock_level = "CanNotDelete"
}

resource "azurerm_storage_container" "backend" {
  name                  = var.container_name
  storage_account_id    = azurerm_storage_account.backend.id
  container_access_type = "private"
}
