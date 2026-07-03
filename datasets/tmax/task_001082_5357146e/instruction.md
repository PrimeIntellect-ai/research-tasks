You are an edge computing engineer tasked with automating the deployment and monitoring of a simulated IoT edge device using a local virtual machine. The device has strict storage limitations, and network access must be carefully mapped.

You must complete the following objectives:

1. **VM Deployment Script**
Create a Bash script at `/home/user/deploy_edge.sh`. This script must launch a QEMU virtual machine with the following specifications:
- Use the binary `qemu-system-x86_64`.
- Use the existing disk image located at `/home/user/images/edge_device.img`.
- Run entirely in the background without any graphical interface (use `-nographic` and `-daemonize`, or equivalent detached execution).
- Allocate exactly 512 Megabytes of RAM.
- Configure user-mode networking with port forwarding: map the host's port `8080` to the guest's port `80` (for web services), and map the host's port `5901` to the guest's port `5900` (for VNC access).

Ensure the script is executable.

2. **Storage Monitoring Script**
The edge device's disk image can grow dynamically. Create a Bash script at `/home/user/check_quota.sh` to monitor its size.
- The script must check the size (in bytes) of `/home/user/images/edge_device.img`.
- If the file size is strictly greater than `104857600` bytes (100 MB), the script must append exactly the following string to `/home/user/alerts.log`:
  `ALERT: Storage limit exceeded - <size> bytes`
  (Replace `<size>` with the actual byte size of the file).
- If the file is 100 MB or smaller, it should do nothing.
- Ensure the script is executable.

3. **Scheduled Execution**
Set up a user-level cron job that executes `/home/user/check_quota.sh` exactly every 15 minutes.
After configuring the crontab, dump the active crontab contents to a file at `/home/user/cron_backup.txt` so your configuration can be verified.

Do not attempt to run the `deploy_edge.sh` script, as the system does not have the necessary virtualization extensions enabled for this simulation; just create the scripts accurately.