variable "proxmox_host" {
    default = "jp-proxmox"
}

variable "webtemplate_name" {
    default = "ubuntu-webserver-cloudinit-template"
}

variable "dbtemplate_name" {
    default = "ubuntu-dbserver-cloudinit-template"
}

variable "template_name" {
    default = "ubuntu-2004-cloudinit-template"
}

variable "dbserver_name" {
    default = "jp-resumedb"
}

variable "dbserver_ip" {
    default = "192.168.69.61"
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

variable "db_vmid" {
    default = "601"
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