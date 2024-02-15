terraform {
  required_providers {
    proxmox = {
      source = "telmate/proxmox"
      version = "3.0.1-rc1"
    }
  }
}

provider "proxmox" {
  pm_api_url = var.proxmox_api_url
  pm_api_token_id = var.proxmox_api_token_id
  pm_api_token_secret = var.proxmox_api_token_secret
  pm_tls_insecure = true
}

resource "proxmox_vm_qemu" "db_server" {
  count = 1 
  name = var.dbserver_name
  vmid = var.db_vmid
  target_node = var.proxmox_host
  clone = var.template_name
  agent = 1
  os_type = "cloud-init"
  cores = 2
  sockets = 1
  cpu = "host"
  memory = 2048
  scsihw = "scsi"
  bootdisk = "scsi0"
  disk {
    size = "10G"
    type = "scsi"
    storage = var.storage_location
    iothread = 1
    ssd = 1
  }

  network {
    model = "virtio"
    bridge = "vmbr0"
  }

  lifecycle {
    ignore_changes = [
      network,
    ]
  }

  ipconfig0 = "ip=192.168.69.61/24,gw=192.168.69.1"
}

resource "proxmox_vm_qemu" "web_server" {
  count = 1 
  name = var.webserver_name
  vmid = var.web_vmid 
  target_node = var.proxmox_host
  clone = var.template_name
  agent = 1
  os_type = "cloud-init"
  cores = 2
  sockets = 1
  cpu = "host"
  memory = 2048
  scsihw = "scsi"
  bootdisk = "scsi0"
  disk {
    size = "10G"
    type = "scsi"
    storage = var.storage_location
    iothread = 1
    ssd = 1
  }

  network {
    model = "virtio"
    bridge = "vmbr0"
  }

  lifecycle {
    ignore_changes = [
      network,
    ]
  }

  ipconfig0 = "ip=192.168.69.62/24,gw=192.168.69.1"
}