terraform {
  required_providers {
    proxmox = {
      source  = "telmate/proxmox"
      version = "3.0.2-rc07"
    }
  }
}

provider "proxmox" {
  pm_api_url          = var.proxmox_api_url
  pm_api_token_id     = var.proxmox_api_token_id
  pm_api_token_secret = var.proxmox_api_token_secret

  # Required for self-signed TLS certificates on the Proxmox host.
  # Replace with a valid CA cert path (pm_tls_insecure = false) if possible.
  pm_tls_insecure = true
}

resource "proxmox_vm_qemu" "web_server" {
  name                    = var.webserver_name
  vmid                    = var.web_vmid
  desc                    = "Web server managed by Terraform"
  tags                    = "webserver,production"
  target_node             = var.proxmox_host
  clone                   = var.webtemplate_name
  onboot                  = true
  cloudinit_cdrom_storage = var.storage_location
  agent                   = 1
  os_type                 = "cloud-init"
  cores                   = var.cpu_cores
  sockets                 = 1
  cpu                     = "host"
  memory                  = var.vm_memory
  scsihw                  = "virtio-scsi-pci"
  bootdisk                = "scsi0"
  boot                    = "order=scsi0;ide3"

  disks {
    scsi {
      scsi0 {
        disk {
          size    = var.disk_size
          storage = var.storage_location
          backup  = true
        }
      }
    }
  }

  network {
    model  = "virtio"
    bridge = "vmbr_srvr"
  }

  lifecycle {
    ignore_changes = [
      network, ciuser, qemu_os, bootdisk
    ]
  }

  ipconfig0 = "ip=${var.webserver_ip}/24,gw=${var.default_gateway}"
}
