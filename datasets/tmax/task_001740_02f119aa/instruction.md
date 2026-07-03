You are a Linux systems engineer tasked with building an automated configuration generator for hardened QEMU Virtual Machines. To streamline deployments, you need to write a Python script that creates safe, standardized configuration snippets for mounting VM disks, configuring timezone settings, setting up administrative email alerts, and generating an interactive bash wrapper to apply them.

Write a Python script at `/home/user/generate_vm_configs.py`. 

Your script must accept exactly three command-line arguments in this order:
1. `vm_name` (e.g., `app_server`)
2. `timezone` (e.g., `UTC` or `Europe/Paris`)
3. `admin_email` (e.g., `admin@example.com`)

When executed, your script must perform the following actions:
1. Ensure the directory `/home/user/configs/` exists.
2. Generate an fstab configuration file at `/home/user/configs/<vm_name>_fstab` containing exactly one line that mounts the QEMU raw image. The format must be:
   `/var/lib/qemu/images/<vm_name>.img /mnt/<vm_name> ext4 loop,noexec,nosuid,nodev 0 0`
3. Generate a postfix/MTA alias snippet at `/home/user/configs/<vm_name>_aliases` for system alerts containing exactly:
   `vm-<vm_name>-alerts: <admin_email>`
4. Generate an interactive shell script at `/home/user/configs/<vm_name>_apply.sh`. This script must:
   - Have the `#!/bin/bash` shebang.
   - Set and export the `TZ` environment variable to the provided `<timezone>`.
   - Prompt the user interactively with exactly: `read -p "Proceed with hardening <vm_name>? (y/n): " confirm`
   - If the user inputs `y`, echo exactly `Hardening applied for <vm_name>`.
   - The script must be made executable (file mode `0755`).

Ensure your Python script strictly matches these output formats so automated integration tests can parse the resulting configuration files. You do not need to execute the generated bash script; simply create it.