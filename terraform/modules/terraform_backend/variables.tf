variable "subscription_id" {
  description = "The subscription ID"
  type        = string
}

variable "resource_group_name" {
  description = "The name of the resource group"
  type        = string
  default     = "tfbackend"
}

variable "location" {
  description = "The location of the resources"
  type        = string
  default     = "germany west central"
}

variable "storage_account_name" {
  description = "The name of the storage account"
  type        = string
  default     = "satfbackendgwc01 "
}

variable "container_name" {
  description = "The name of the storage container"
  type        = string
  default     = "tfbackend"
}
