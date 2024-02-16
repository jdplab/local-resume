variable "proxmox_host" {
    default = "jp-proxmox"
}

variable "webtemplate_name" {
    default = "ubuntu-webserver-cloudinit-template"
}

variable "webserver_name" {
    default = "jp-resumeweb"
}

variable "webserver_ip" {
    default = "192.168.69.62"
}

variable "proxmox_api_url" {
    default = "https://192.168.69.251:8006/api2/json"
}

variable "proxmox_api_token_id" {
    default = "terraform-prov@pve!terraformToken"
}

variable "proxmox_api_token_secret" {
    default = "a7b5c294-5bbf-4736-aa6a-ce0d23616307"
}

variable "web_vmid" {
    default = "602"
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
    default = "JP12345!"
}

variable "disk_size" {
    default = 10
}