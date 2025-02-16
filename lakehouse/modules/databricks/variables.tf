variable "resource_group_name" {
  description = "The name of the resource group."
  type        = string
}

variable "location" {
  description = "Azure region for resources."
  type        = string
}

variable "vnet_name" {
  description = "Name of the virtual network."
  type        = string
}

variable "vnet_address_space" {
  description = "Address space for the virtual network."
  type        = list(string)
}

variable "subnet_name" {
  description = "Name of the subnet for Databricks."
  type        = string
}

variable "subnet_address_prefix" {
  description = "Address prefix for the subnet."
  type        = list(string)
}

variable "databricks_workspace_name" {
  description = "Name of the Databricks workspace."
  type        = string
}

variable "private_endpoint_name" {
  description = "Name of the private endpoint."
  type        = string
}
