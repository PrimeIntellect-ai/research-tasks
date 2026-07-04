You are tasked with building the foundation of a local Kubernetes-like operator that manages lightweight VMs using QEMU. You need to create several scripts and configurations to handle connectivity diagnostics, backups, disk provisioning, and VM launching. 

All your work must be done in `/home/user`. Do not use `sudo` or root privileges.

Perform the following steps:

1. **Connectivity Diagnostics (Python)**
There is a log file at `/home/user/connection.log` (you do not need to read a real one, just assume the automated test will provide it). It contains mock SSH debug output where one specific IP address silently rejects key-based login. The log lines look like this:
`debug1: Connecting to 192.168.1.50 [192.168.1.50] port 22.`
`debug1: receive packet: type 51` (which means failure).
Write a Python script `/home/user/diagnose.py` that reads `connection.log`, finds the IP address on the line immediately preceding a `type 51` packet, and prints ONLY that IP address to standard output.

2. **Backup Strategy (Shell)**
Write a bash script `/home/user/backup.sh` that creates a gzip-compressed tarball of the directory `/home/user/manifests` (assume this directory exists). The backup must be saved exactly as `/home/user/manifests_backup.tar.gz`.

3. **Fstab Configuration**
Create a text file `/home/user/new_fstab` that contains exactly one valid `/etc/fstab` entry to mount a filesystem with the label `vmdatalocal` to the mount point `/var/lib/vmdata`. It must use the `ext4` filesystem, with the options `rw,noatime`, and dump/pass values of `0 2`.

4. **Storage Provisioning (Shell)**
Create a bash script `/home/user/provision_disk.sh` that creates a blank 50MB raw disk image at `/home/user/vm_disk.img` and formats it as an `ext4` filesystem. This must be done without root access (hint: use `dd` or `truncate` and `mkfs.ext4 -F`).

5. **VM Management (Shell)**
Write a bash script `/home/user/launch_qemu.sh` that launches a QEMU VM in the background. The command must:
- Use `qemu-system-x86_64`
- Run without a default graphical UI (`-nographic` or `-display none`)
- Expose a VNC server on display `:2` (port 5902)
- Attach the disk `/home/user/vm_disk.img` as a `virtio` block device.
- Save the process ID (PID) of the QEMU process to `/home/user/qemu.pid`.

Make sure all your bash and python scripts are executable (`chmod +x`). 
You do not need to run the `launch_qemu.sh` script, just write it correctly.