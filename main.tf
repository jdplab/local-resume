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

resource "proxmox_vm_qemu" "web_server" {
  count = 1 
  name = var.webserver_name
  vmid = var.web_vmid
  target_node = var.proxmox_host
  clone = var.webtemplate_name
  onboot = true
  cloudinit_cdrom_storage = var.storage_location
  agent = 1
  os_type = "cloud-init"
  cores = var.cpu_cores
  sockets = 1
  cpu = "host"
  memory = var.vm_memory
  scsihw = "virtio-scsi-pci"
  bootdisk = "scsi0"
  boot = "order=scsi0;ide3"
  disks {
    scsi {
      scsi0 {
        disk {
          size = var.disk_size
          storage = var.storage_location
          backup = false
        }
      }
    }
  }
  network {
    model = "virtio"
    bridge = "vmbr0"
  }
  lifecycle {
    ignore_changes = [
      network,ciuser,qemu_os,bootdisk
    ]
  }
  ipconfig0 = "ip=${var.webserver_ip}/24,gw=192.168.69.1"
}
