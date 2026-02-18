output "vm_name" {
  description = "Name of the provisioned web server VM"
  value       = proxmox_vm_qemu.web_server.name
}

output "vm_id" {
  description = "Proxmox VM ID of the provisioned web server"
  value       = proxmox_vm_qemu.web_server.vmid
}

output "vm_ip" {
  description = "IP address assigned to the web server"
  value       = var.webserver_ip
}
