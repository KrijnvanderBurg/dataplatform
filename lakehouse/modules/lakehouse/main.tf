module "source" {
  source = "../datalake"
  environment = var.environment
  sequence_number = "01"
  subscription_id = var.subscription_id
  resource_group_name = var.resource_group_name
  location_primary = var.source_location_primary
  location_primary_abbr = var.source_location_primary_abbr
  storage_account_name = var.source_storage_account_name
  account_replication_type = var.source_account_replication_type
  containers = var.source_containers
}
