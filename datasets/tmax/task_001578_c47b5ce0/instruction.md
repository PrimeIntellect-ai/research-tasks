You are a monitoring specialist tasked with setting up an automated alerting and logging configuration bundle for a legacy system. You do not have root access, so you will prepare configuration files in your home directory and write a local monitoring script that simulates interactions with a legacy service.

Complete the following objectives:

1. **Expect-based Python Monitor:**
   There is a legacy mock service located at `/home/user/legacy_service.sh`. It requires interactive authentication.
   Write a Python script at `/home/user/monitor.py` that uses the `pexpect` module to do the following:
   - Spawn `/home/user/legacy_service.sh`.
   - Wait for the prompt exactly matching `"Enter monitor password: "`.
   - Send the password `"alertadmin"`.
   - Capture the resulting output line which will look like `"STATUS: <SOMESTATUS>"`.
   - Append a strictly formatted JSON line to the log file `/home/user/app_logs/monitor.log`. The JSON should have two keys: `"event"` (always set to `"service_check"`) and `"status"` (containing the exact parsed `<SOMESTATUS>` value, e.g., `"CRITICAL"`).
   - Ensure `/home/user/app_logs` exists before writing.

2. **Log Rotation Configuration:**
   Create a standard `logrotate` configuration file at `/home/user/monitor_logrotate.conf` to manage the `/home/user/app_logs/monitor.log` file.
   It must contain the following directives explicitly:
   - Rotate when the file size reaches `10k`.
   - Keep `4` rotated logs.
   - Use `compress` for old logs.
   - Recreate the file with permissions `0644` (you do not need to specify user/group).
   - `missingok` and `notifempty`.

3. **Storage Mount Configuration:**
   We need to mount a remote NFS share for backups, but you only need to prepare the fstab line.
   Create a file at `/home/user/backup.fstab` containing exactly ONE line formatted for `/etc/fstab` that does the following:
   - Remote source: `10.50.0.5:/export/backups`
   - Mount point: `/home/user/remote_backups`
   - Filesystem type: `nfs`
   - Options: `ro,user,noauto,hard`
   - Dump and pass values: `0 0`

4. **Firewall Port Forwarding Rule:**
   Write the exact `iptables` command required to perform port forwarding (Destination NAT) for incoming TCP traffic.
   Save this single command to `/home/user/port_forward.sh`.
   Requirements:
   - Table: `nat`
   - Chain: `PREROUTING`
   - Interface: `eth1`
   - Protocol: `tcp`
   - Destination port: `80`
   - Target: `DNAT`
   - To-destination: `192.168.1.100:8080`

Execute your `monitor.py` script once successfully so the `/home/user/app_logs/monitor.log` file is generated with the correct JSON payload.