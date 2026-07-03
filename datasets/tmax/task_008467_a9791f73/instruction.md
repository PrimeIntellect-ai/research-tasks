You are a FinOps analyst tasked with optimizing and estimating cloud costs for a legacy regional infrastructure setup.

Your task consists of two parts: analyzing network storage costs using a Rust program, and configuring a script to spin up a lightweight virtual machine for regional billing simulation.

**Part 1: Network Storage Cost Calculation**
We have a mock fstab file located at `/home/user/cloud_fstab` which lists the mount points currently used by our instances. 
You need to create a Rust project at `/home/user/finops_calc` and write a program in `/home/user/finops_calc/src/main.rs` that reads `/home/user/cloud_fstab`.
The program must calculate the total monthly cost of network mounts based on the filesystem type specified in the fstab:
- Every `nfs` mount costs 120 credits.
- Every `cifs` mount costs 85 credits.
- All other filesystem types (e.g., `ext4`, `xfs`) cost 0 credits.

Your Rust program should write the final total cost as a plain integer to `/home/user/network_storage_cost.txt`.
Make sure to initialize the Rust project with `cargo init` and ensure it runs successfully.

**Part 2: Regional VM Configuration**
We need to simulate the billing environment in a specific timezone using a lightweight QEMU VM.
Write a bash script at `/home/user/run_billing_vm.sh` that launches a QEMU virtual machine in the background (`-daemonize` or using `&`) with the following exact specifications:
1. Use `qemu-system-x86_64`.
2. Allocate exactly 128MB of RAM (`-m 128`).
3. Boot the kernel located at `/home/user/bzImage` (this file will be present on the system).
4. Expose the VM's display via VNC on display number `:2` (which corresponds to port 5902).
5. Pass the timezone configuration to the Linux kernel via the `-append` flag. The kernel parameters must include `TZ=Europe/London`.

Make sure `/home/user/run_billing_vm.sh` is executable. You do not need to run the script, just create it perfectly so our automated systems can execute it.