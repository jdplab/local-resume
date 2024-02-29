variable "proxmox_host" {
    default = "jp-proxmox"
}

variable "webtemplate_name" {
    default = "ubuntu-webserver-cloudinit-template"
}

variable "webserver_name" {
    type = string
}

variable "webserver_ip" {
    type = string
}

variable "proxmox_api_url" {
    type = string
}

variable "proxmox_api_token_id" {
    type = string
}

variable "proxmox_api_token_secret" {
    type = string
}

variable "web_vmid" {
    type = string
}

variable "storage_location" {
    default = "local-lvm"
}

variable "ssh_port" {
    default = 22
}

variable "ssh_user" {
    default = "root"
}

variable "ssh_pw" {
    type = string
}

variable "disk_size" {
    default = 10
}

variable "cpu_cores" {
    type = string
}

variable "vm_memory" {
    type = string
}