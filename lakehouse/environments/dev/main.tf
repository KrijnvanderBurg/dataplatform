provider "azurerm" {
  subscription_id = var.subscription_id
  tenant_id = var.tenant_id
  use_oidc = true
  features {}
}

module "lakehouse" {
  source           = "../../modules/lakehouse"
  vnet_hub_cidr          = var.vnet_hub_cidr
  vnet_spoke_cidr        = var.vnet_spoke_cidr
  location       = var.location
  metastoreip      = var.metastoreip
  dbfs_prefix      = var.dbfs_prefix
  workspace_prefix = var.workspace_prefix
  firewallfqdn     = var.firewallfqdn
}

output "workspace_url" {
  value = module.lakehouse.workspace_url
}

output "workspace_azure_resource_id" {
  value = module.lakehouse.databricks_azure_workspace_resource_id
}

output "test_vm_public_ip" {
  value = module.lakehouse.test_vm_public_ip
}

output "resource_group" {
  value = module.lakehouse.resource_group
}
