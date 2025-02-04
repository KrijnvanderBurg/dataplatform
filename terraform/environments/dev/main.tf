module "terraform_backend" {
  source              = "../../modules/terraform_backend"
  subscription_id     = var.subscription_id
  resource_group_name = var.resource_group_name
  location            = var.location
  storage_account_name = var.storage_account_name
  container_name      = var.container_name
}

// Include shared variables
# ...existing code...
