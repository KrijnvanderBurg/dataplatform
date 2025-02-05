provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
  tenant_id       = var.tenant_id
}

terraform {
  backend "local" {
    path = "remote_backend.tfstate"
  }
}

module "remote_backend" {
  source                = "../../modules/remote_backend"
  subscription_id       = var.subscription_id
  environment           = var.environment
  location_primary      = var.location_primary
  location_primary_abbr = var.location_primary_abbr
}
