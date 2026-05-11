variable "resource_group_name" {
  description = "Name of the Azure Resource Group"
  type        = string
  default     = "dtp-rg"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "polandcentral"
}

variable "admin_username" {
  description = "VM admin username"
  type        = string
  default     = "azureuser"
}
