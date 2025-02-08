variable "subscription_id" {
    type = string
}

variable "environment" {
    type = string
}

variable "sequence_number" {
    type = string
}

variable "resource_group_name" {
  type = string
}

variable "storage_account_name" {
    type = string
}

variable "location_primary" {
    type = string
}

variable "location_primary_abbr" {
    type = string
}

variable "account_replication_type" {
    type = string
}

variable "containers" {
    type = set(string)
}