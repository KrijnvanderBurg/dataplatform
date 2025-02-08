variable "subscription_id" {
    type = string
}

variable "resource_group_name" {
    type = string
}

# source layer
variable "source_location_primary" {
  type = string
}

variable "source_location_primary_abbr" {
  type = string
}

variable "source_storage_account_name" {
  type = string
}

variable "source_account_replication_type" {
  type = string
}

variable "source_containers" {
  type = list(string)
}
