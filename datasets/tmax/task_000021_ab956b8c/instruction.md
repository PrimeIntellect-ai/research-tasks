You are tasked with fixing and enhancing a custom Bash-based "Kubernetes-style" VM operator. This script, `/home/user/vm-operator.sh`, is responsible for reading VM manifest files, setting up network port forwarding, and launching QEMU virtual machines. However, it currently has several critical flaws involving startup dependencies, missing restart policies, and lack of configuration backups.

Your goal is to modify `/home/user/vm-operator.sh` to meet the following requirements:

1. **Fix the Startup Dependency (Missing After= logic):** 
   The operator currently attempts to start VMs immediately. It must be modified to wait until the network routing subsystem is ready. Before reading any manifests, the script must poll every 1 second until the file `/home/user/network/routing.ready` exists. While waiting, it should append the exact string `WAITING FOR NETWORK` to `/home/user/operator.log` once per check.

2. **Implement Manifest Backups:**
   Before processing any manifest file (`*.conf`) found in `/home/user/manifests/`, the operator must copy the file to `/home/user/backups/`. The backed-up filename must be `<original-filename>.<timestamp>.bak` (where timestamp is the output of `date +%s`). If `/home/user/backups/` does not exist, the operator must create it.

3. **Configure QEMU Networking & Routing:**
   The operator reads manifest files formatted as key-value pairs (e.g., `VM_NAME=web`, `HOST_PORT=8080`, `VM_PORT=80`). You must construct the correct QEMU command using user-mode networking to forward the host port to the VM port. 
   The command to execute must be EXACTLY:
   `qemu-system-x86_64 -m 256 -name <VM_NAME> -netdev user,id=net0,hostfwd=tcp:127.0.0.1:<HOST_PORT>-:<VM_PORT> -device e1000,netdev=net0`
   (Replace the bracketed variables with the values parsed from the manifest).

4. **Implement a Restart Policy (Process Supervision):**
   Instead of just running the QEMU command once, the operator must supervise the process. 
   - It should run the constructed QEMU command.
   - If the command exits with a non-zero exit code, it must append `RESTARTING <VM_NAME>` to `/home/user/operator.log` and restart the command.
   - It should attempt a maximum of 3 restarts (i.e., 4 total runs) per VM if it keeps failing. If it exits with code 0, do not restart.
   - For this task, handle one manifest sequentially (no need to background the tasks).

Ensure your script writes all necessary output to `/home/user/operator.log`. Do not write the actual `qemu-system-x86_64` binary to disk; assume it is available in the `$PATH` (a mock will be provided during automated testing).

**Initial setup instructions:**
You must create the basic directory structure to begin your work:
`mkdir -p /home/user/manifests /home/user/network`
Then create a test manifest at `/home/user/manifests/app.conf`:
```
VM_NAME=backend
HOST_PORT=9090
VM_PORT=3000
```
Write your complete `vm-operator.sh` script in `/home/user/` and ensure it is executable.