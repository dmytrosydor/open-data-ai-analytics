output "public_ip" {
  description = "Public IP address of the VM"
  value       = azurerm_public_ip.pip.ip_address
}

output "private_key" {
  description = "SSH private key for VM access"
  value       = tls_private_key.ssh.private_key_openssh
  sensitive   = true
}
