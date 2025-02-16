variable "vnet_id" {
  description = "The ID of the virtual network to attach the VPN gateway."
  type        = string
}

variable "environment" {
  description = "The environment for the resources."
  type        = string
}

variable "gateway_subnet_address_prefix" {
  description = "The address prefix for the gateway subnet."
  type        = list(string)
}

variable "onprem_vpn_gateway_ip" {
  description = "The public IP of the on-prem VPN gateway."
  type        = string
}

variable "onprem_address_space" {
  description = "The address space of the on-prem network."
  type        = list(string)
}

variable "vpn_shared_key" {
  description = "The shared key for the VPN connection."
  type        = string
}
