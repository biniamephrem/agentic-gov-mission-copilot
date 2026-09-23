terraform {
  required_version = ">= 1.6.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "main" {
  name     = "${var.name}-rg"
  location = var.location
}

resource "azurerm_storage_account" "evidence" {
  name                     = replace("${var.name}data", "-", "")
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  min_tls_version          = "TLS1_2"
  public_network_access_enabled = false
}

resource "azurerm_key_vault" "main" {
  name                       = "${var.name}-kv"
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  tenant_id                  = var.tenant_id
  sku_name                   = "standard"
  purge_protection_enabled   = true
  soft_delete_retention_days = 90
}

# Production expansion points:
# - Azure OpenAI / Azure AI Foundry
# - Azure AI Search
# - Azure Container Apps or AKS
# - Cosmos DB for mission state
# - Private Endpoints / Private DNS
# - Log Analytics / Application Insights / Microsoft Sentinel
