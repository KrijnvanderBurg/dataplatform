variable "resource_group_name" {
  description = "The name of the resource group"
  type        = string
  default     = "prod-rg"
}

variable "location" {
  description = "The location of the resources"
  type        = string
  default     = "East US"
}

variable "storage_account_name" {
  description = "The name of the storage account"
  type        = string
  default     = "prodstorageacct"
}

variable "container_name" {
  description = "The name of the storage container"
  type        = string
  default     = "prodcontainer"
}

variable "subscription_id" {
  description = "The subscription ID"
  type        = string
}
