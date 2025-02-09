terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 4.1.0"
        }
      }
  # backend "azurerm" {
  #   resource_group_name  = "rg-init-dev-gwc-01"
  #   storage_account_name = "sttfbackenddevgwc01"
  #   container_name       = "tfstate"
  #   key                  = "lakehouse.tfstate"
  #   use_oidc             = true
  # }
}

provider "azurerm" {
  subscription_id = var.subscription_id
  tenant_id = var.tenant_id
  use_oidc = true
  features {}
}


resource "azurerm_resource_group" "storage" {
  name     = "rg-storage-${var.environment}-${var.location_primary_abbr}-01"
  location = var.location_primary
}

module "source_datalake" {
  source                          = "../../modules/lakehouse"
  sequence_number                 = "01"
  environment                     = var.environment
  subscription_id                 = var.subscription_id
  resource_group_name             = azurerm_resource_group.storage.name
  source_location_primary         = var.location_primary
  source_location_primary_abbr    = var.location_primary_abbr
  source_storage_account_name     = "source"
  source_account_replication_type = "ZRS"
  source_containers               = ["test"]
}
