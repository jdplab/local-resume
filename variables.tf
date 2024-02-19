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
    default = "https://192.168.69.251:8006/api2/json"
}

variable "proxmox_api_token_id" {
    default = "terraform-prov@pve!terraformToken"
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

variable "ipconfig_settings" {
    type = string
}