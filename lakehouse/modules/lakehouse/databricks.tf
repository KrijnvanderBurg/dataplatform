resource "azurerm_databricks_workspace" "this" {
  name                                  = "dbw-main"
  resource_group_name                   = azurerm_resource_group.this.name
  location                              = azurerm_resource_group.this.location
  sku                                   = "premium"
  tags                                  = local.tags
  public_network_access_enabled         = false                    //use private endpoint
  network_security_group_rules_required = "NoAzureDatabricksRules" //use private endpoint
  customer_managed_key_enabled          = true
  //infrastructure_encryption_enabled = true
  custom_parameters {
    no_public_ip                                         = true
    virtual_network_id                                   = azurerm_virtual_network.this.id
    private_subnet_name                                  = azurerm_subnet.private.name
    public_subnet_name                                   = azurerm_subnet.public.name
    public_subnet_network_security_group_association_id  = azurerm_subnet_network_security_group_association.public.id
    private_subnet_network_security_group_association_id = azurerm_subnet_network_security_group_association.private.id
    storage_account_name                                 = local.dbfsname
  }
  # We need this, otherwise destroy doesn't cleanup things correctly
  depends_on = [
    azurerm_subnet_network_security_group_association.public,
    azurerm_subnet_network_security_group_association.private
  ]
}


resource "azurerm_firewall_network_rule_collection" "adbfnetwork" {
  name                = "afwp-adbcontrolplanenetwork"
  azure_firewall_name = azurerm_firewall.hubfw.name
  resource_group_name = azurerm_resource_group.this.name
  priority            = 200
  action              = "Allow"

  rule {
    name = "databricks-metastore"

    source_addresses = [
      join(", ", azurerm_subnet.public.address_prefixes),
      join(", ", azurerm_subnet.private.address_prefixes),
    ]

    destination_ports = [
      "3306",
    ]

    destination_addresses = [
      var.metastoreip,
    ]

    protocols = [
      "TCP",
    ]
  }
}

resource "azurerm_firewall_application_rule_collection" "adbfqdn" {
  name                = "afwp-adbcontrolplanefqdn"
  azure_firewall_name = azurerm_firewall.hubfw.name
  resource_group_name = azurerm_resource_group.this.name
  priority            = 200
  action              = "Allow"

  rule {
    name = "databricks-control-plane-services"

    source_addresses = [
      join(", ", azurerm_subnet.public.address_prefixes),
      join(", ", azurerm_subnet.private.address_prefixes),
    ]

    target_fqdns = var.firewallfqdn

    protocol {
      port = "443"
      type = "Https"
    }
  }
}

resource "azurerm_route_table" "adbroute" {
  //route all traffic from spoke vnet to hub vnet
  name                = "spoke-routetable"
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name

  route {
    name                   = "to-firewall"
    address_prefix         = "0.0.0.0/0"
    next_hop_type          = "VirtualAppliance"
    next_hop_in_ip_address = azurerm_firewall.hubfw.ip_configuration.0.private_ip_address // extract single item
  }
}

resource "azurerm_subnet_route_table_association" "publicudr" {
  subnet_id      = azurerm_subnet.public.id
  route_table_id = azurerm_route_table.adbroute.id
}

resource "azurerm_subnet_route_table_association" "privateudr" {
  subnet_id      = azurerm_subnet.private.id
  route_table_id = azurerm_route_table.adbroute.id
}
