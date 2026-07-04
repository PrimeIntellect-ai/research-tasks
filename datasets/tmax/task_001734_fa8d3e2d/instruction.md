You are acting as a FinOps analyst tasked with optimizing cloud storage costs. We have a pool of virtual machine disk images, but some of the VMs are completely disconnected from the network and are no longer actively used. Keeping their raw disks on hot storage is expensive.

Your task is to identify these disconnected VMs, back up their disk images to cold storage, and generate a cleanup report.

Here are the specifics:
1. There is a VM manifest located at `/home/user/vm_data/manifest.json`. This file contains an array of VM objects. Each object has:
   - `vm_id`: The name of the virtual machine.
   - `disk_image`: The filename of the VM's disk (located in `/home/user/vm_data/disks/`).
   - `connections`: A list of network endpoints the VM is actively connected to.

2. A VM is considered "disconnected" if its `connections` list is entirely empty.

3. You must identify all disconnected VMs. For each disconnected VM, back up its corresponding disk image by adding it to a single compressed tar archive located at `/home/user/cold_storage/orphaned_disks_backup.tar.gz`.
   * Note: The tar archive should only contain the disk files themselves, not the parent directory structure (do not include `home/user/vm_data/disks/` in the archive paths).

4. Finally, generate a report file at `/home/user/finops_report.txt`. This file must contain the exact `vm_id`s of all the disconnected VMs you backed up, with exactly one `vm_id` per line, sorted in alphabetical order.

You may write a script in Python, Bash, or any combination of tools to achieve this.