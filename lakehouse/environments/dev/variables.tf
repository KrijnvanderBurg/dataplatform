variable "tenant_id" {
type = string
}

variable "subscription_id" {
  type = string
}

variable "environment" {
  type = string
}

variable "resource_group_name_storage" {
  type = string
}

variable "resource_group_name_databricks" {
  type = string
}

variable "resource_group_name_network" {
  type = string
}

variable "vnet_hub_cidr" {
  type        = string
  default     = "10.178.0.0/16"
  description = "CIDR for Hub VNet"
}

variable "vnet_spoke_cidr" {
  type        = string
  default     = "10.179.0.0/16"
  description = "CIDR for Spoke VNet"
}

variable "location" {
  type        = string
  default     = "southeastasia"
  description = "Location of resource group to create"
}


variable "dbfs_prefix" {
  type        = string
  default     = "dbfs"
  description = "Prefix for DBFS storage account name"
}

variable "workspace_prefix" {
  type        = string
  default     = "adb"
  description = "Prefix to use for Workspace name"
}


variable "metastoreip" {
  type        = string
  description = "IP Address of built-in Hive Metastore in the target region"
}


variable "firewallfqdn" {
  type        = list(any)
  description = "Additional list of fully qualified domain names to add to firewall rules"
}