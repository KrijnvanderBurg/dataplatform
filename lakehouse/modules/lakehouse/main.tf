terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.104.0"
    }
  }
}
locals {
  dbfsname = "a847bfh" // dbfs name must not have special chars
  rg_network_name = "rg-network-${var.environment}-${var.location_short}"

  // tags that are propagated down to all resources
  tags = merge({
    Owner = "Krijn van der Burg"
  }, var.tags)
}

resource "azurerm_resource_group" "this" {
  name     = "adb-dev-test-rg"
  location = var.location
  tags     = local.tags
}
