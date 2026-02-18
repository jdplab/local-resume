variable "proxmox_host" {
  description = "Name of the Proxmox node to deploy the VM on"
  type        = string
  default     = "pve"
}

variable "webtemplate_name" {
  description = "Name of the Proxmox VM template to clone"
  type        = string
  default     = "ubuntu-webserver-cloudinit-template"
}

variable "webserver_name" {
  description = "Name assigned to the web server VM in Proxmox"
  type        = string
}

variable "webserver_ip" {
  description = "Static IPv4 address to assign to the web server (without prefix length)"
  type        = string

  validation {
    condition     = can(regex("^(\\d{1,3}\\.){3}\\d{1,3}$", var.webserver_ip))
    error_message = "webserver_ip must be a valid IPv4 address (e.g. 192.168.1.10)."
  }
}

variable "default_gateway" {
  description = "Default gateway IPv4 address for the web server network"
  type        = string

  validation {
    condition     = can(regex("^(\\d{1,3}\\.){3}\\d{1,3}$", var.default_gateway))
    error_message = "default_gateway must be a valid IPv4 address (e.g. 192.168.1.1)."
  }
}

variable "proxmox_api_url" {
  description = "Full URL of the Proxmox API endpoint (e.g. https://pve.example.com:8006/api2/json)"
  type        = string
}

variable "proxmox_api_token_id" {
  description = "Proxmox API token ID in the format user@realm!tokenname"
  type        = string
}

variable "proxmox_api_token_secret" {
  description = "Proxmox API token secret value"
  type        = string
  sensitive   = true
}

variable "web_vmid" {
  description = "Proxmox VM ID to assign to the web server (must be 100–999999999)"
  type        = number

  validation {
    condition     = var.web_vmid >= 100 && var.web_vmid <= 999999999
    error_message = "web_vmid must be between 100 and 999999999."
  }
}

variable "storage_location" {
  description = "Name of the Proxmox storage pool used for the VM disk and cloud-init drive"
  type        = string
  default     = "VM-Data"
}

variable "ssh_port" {
  description = "SSH port used when connecting to the VM for provisioning"
  type        = number
  default     = 22
}

variable "ssh_user" {
  description = "SSH username used when connecting to the VM for provisioning"
  type        = string
  default     = "root"
}

variable "ssh_pw" {
  description = "SSH password used when connecting to the VM for provisioning"
  type        = string
  sensitive   = true
}

variable "disk_size" {
  description = "Size of the VM boot disk in gigabytes"
  type        = number
  default     = 10
}

variable "cpu_cores" {
  description = "Number of CPU cores to assign to the VM"
  type        = number
}

variable "vm_memory" {
  description = "Amount of RAM to assign to the VM in megabytes"
  type        = number
}
