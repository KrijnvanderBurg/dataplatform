variable "resource_group_name" {
  description = "Resource group name"
  type        = string
}

variable "hub_vnet_name" {
  description = "Hub virtual network name"
  type        = string
}

variable "hub_vnet_address_space" {
  description = "Address space for hub VNet"
  type        = list(string)
}

variable "spoke_vnet_name" {
  description = "Spoke virtual network name"
  type        = string
}

variable "spoke_vnet_address_space" {
  description = "Address space for spoke VNet"
  type        = list(string)
}