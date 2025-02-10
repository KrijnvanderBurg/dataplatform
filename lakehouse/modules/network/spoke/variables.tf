variable "resource_group_name" {
  description = "Resource group name"
  type        = string
}

variable "location" {
  description = "Azure location"
  type        = string
}

variable "sequence_number" {
  type        = number
}

variable "environment" {
  type        = string
}

variable "rg_name" {
  description = "Resource group name for the spoke"
  type        = string
}

variable "vnet_name" {
  description = "Spoke virtual network name"
  type        = string
}

variable "vnet_address_space" {
  description = "Address space for spoke VNet"
  type        = list(string)
}

variable "hub_vnet_id" {
  description = "The ID of the hub virtual network"
  type        = string
}
