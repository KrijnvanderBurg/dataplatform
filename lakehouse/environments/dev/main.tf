/**
 * Azure Databricks workspace in custom VNet
 *
 * Module creates:
 * * Resource group with random prefix
 * * Tags, including `Owner`, which is taken from `az account show --query user`
 * * VNet with public and private subnet
 * * Databricks workspace
 */

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.104.0"
    }
    random = {
      source = "hashicorp/random"
    }
  }
}

provider "azurerm" {
  subscription_id = var.subscription_id
  tenant_id = var.tenant_id
  use_oidc = true
  features {}
}

module "adb_with_private_links_exfiltration_protection" {
  source           = "./modules/adb-with-private-links-exfiltration-protection"
  vnet_hub_cidr          = var.vnet_hub_cidr
  vnet_spoke_cidr        = var.vnet_spoke_cidr
  location       = var.location
  dbfs_prefix      = var.dbfs_prefix
  workspace_prefix = var.workspace_prefix
}

output "workspace_url" {
  value = module.adb_with_private_links_exfiltration_protection.workspace_url
}

output "workspace_azure_resource_id" {
  value = module.adb_with_private_links_exfiltration_protection.databricks_azure_workspace_resource_id
}

output "test_vm_public_ip" {
  value = module.adb_with_private_links_exfiltration_protection.test_vm_public_ip
}

output "resource_group" {
  value = module.adb_with_private_links_exfiltration_protection.resource_group
}
