resource "azurerm_storage_account" "source" {
  name                     = "source"
  resource_group_name      = var.resource_group_name
  location                 = var.location_primary
  account_tier             = "Standard"
  account_replication_type = var.bronze_account_replication_type

  lifecycle {
    prevent_destroy = true
  }
}

resource "azurerm_management_lock" "source_lock" {
  name        = "lock-source"
  scope       = azurerm_storage_account.source.id
  lock_level  = "CanNotDelete"
  notes       = "Source data may not be deleted under any circumstance."
}

resource "azurerm_storage_container" "container" {
  name                  ="gw2api"
  storage_account_id    = azurerm_storage_account.source.id
  container_access_type = "private"

  lifecycle {
    prevent_destroy = true
  }
}