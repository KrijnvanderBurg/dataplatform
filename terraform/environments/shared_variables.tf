variable "resource_group_name" {
  description = "The name of the resource group"
  type        = string
  default     = "default-rg"
}

variable "location" {
  description = "The location of the resources"
  type        = string
  default     = "East US"
}

variable "storage_account_name" {
  description = "The name of the storage account"
  type        = string
  default     = "defaultstorageacct"
}

variable "container_name" {
  description = "The name of the storage container"
  type        = string
  default     = "defaultcontainer"
}
