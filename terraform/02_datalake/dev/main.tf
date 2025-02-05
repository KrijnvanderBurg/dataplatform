locals {
  subscription_id = "6867b85b-e868-4d21-a71a-0f82b27117b9"
  tenant_id       = "9e8cdb6a-eda5-4cca-8b83-b40f0074d999"
}

provider "azurerm" {
  features {}
  subscription_id = local.subscription_id
  tenant_id       = local.tenant_id
}

terraform {
  backend "local" {
    path = "terraform.tfstate"
  }
}

module "terraform_backend" {
  source               = "../../modules/terraform_backend"
  subscription_id      = "6867b85b-e868-4d21-a71a-0f82b27117b9"
  resource_group_name  = "tfbackend"
  location             = "germany west central"
  storage_account_name = "tfbackend"
  container_name       = "tfbackend"
}

resource "azurerm_resource_group" "storage" {
  name = "storage"
  location = "germany west central"
}

module "datalake" {
  source               = "../../modules/datalake"
  subscription_id      = "6867b85b-e868-4d21-a71a-0f82b27117b9"
  resource_group_name  = azurerm_resource_group.storage.name
  location_primary     = "germany west central"
  bronze_account_replication_type = "ZRS"
}
