As a cloud architect migrating services to a modern infrastructure, you are temporarily running a "hybrid" environment. You need to write a deployment script that provisions a legacy VM (using QEMU), sets up its log rotation, injects environment variables, and launches a robust shim script simulating a new containerized service.

Write a Bash script at `/home/user/setup_hybrid.sh` that accomplishes the following tasks when executed:

1. **Environment Setup**: 
   Append the following environment variables to `/home/user/.profile`:
   - `MIGRATION_PHASE=hybrid`
   - `QEMU_VNC_DISPLAY=:5`

2. **Legacy VM Virtualization**:
   Launch a QEMU VM in the background using `qemu-system-x86_64`.
   - Use the existing dummy disk image at `/home/user/legacy.img`.
   - Configure VNC to run on display `:5` (using `-vnc :5`).
   - Redirect the serial console output to a file at `/home/user/legacy_vm.log` (using `-serial file:/home/user/legacy_vm.log`).
   - Ensure it detaches from the terminal (e.g., using `-daemonize` or running in the background).

3. **Log Configuration & Rotation**:
   Create a logrotate configuration file at `/home/user/vm_logrotate.conf` specifically for `/home/user/legacy_vm.log`.
   It must specify the following rules:
   - Rotate `hourly`
   - Keep `5` rotations (`rotate 5`)
   - Compress old log files (`compress`)
   - Ignore missing log files (`missingok`)
   After generating the file, your script must force an immediate logrotate run using this config:
   `logrotate -f -s /home/user/logrotate.status /home/user/vm_logrotate.conf`

4. **Container Lifecycle Shim**:
   Create a robust Bash script at `/home/user/container_shim.sh` that simulates the lifecycle of our next-gen containerized service. 
   - It must be executable.
   - Upon startup, it must append the exact string `[INFO] Starting next-gen service` to `/home/user/nextgen.log`.
   - It must trap `SIGTERM` and `SIGINT`. When either signal is received, it must append the exact string `[INFO] Shutting down gracefully` to `/home/user/nextgen.log` and then cleanly exit with code `0`.
   - It should remain running in an infinite loop (e.g., `while true; do sleep 1; done`) until a signal is caught.

5. **Shim Execution**:
   Finally, your `/home/user/setup_hybrid.sh` script must launch `/home/user/container_shim.sh` in the background and save its Process ID (PID) into the file `/home/user/container_shim.pid`.

Ensure your `setup_hybrid.sh` script is executable and run it to set up the system.