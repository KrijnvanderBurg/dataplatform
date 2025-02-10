output "vpn_gateway_public_ip" {
  description = "The public IP of the VPN gateway."
  value       = azurerm_public_ip.vpn_gateway_ip.ip_address
}
