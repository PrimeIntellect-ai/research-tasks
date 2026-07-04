You are a capacity planner analyzing resource usage across a distributed system. To safely gather and process remote metrics, you need to prepare an environment setup script that prepares log management, defines network mounts, and establishes a secure tunnel command.

Since you do not have root access on this analysis node, you are preparing configuration files and command snippets that can be reviewed or executed locally.

Write a bash script at `/home/user/capacity_setup.sh` that, when executed, performs the following exact steps:

1. **Log Rotation Configuration**:
   Create a logrotate configuration file at `/home/user/logrotate.conf` targeting the log file `/home/user/capacity_logs/usage.log`. The configuration must specify:
   - `weekly` rotation
   - keep exactly `4` backups (`rotate 4`)
   - `compress` old logs
   - ignore missing files (`missingok`)

2. **Fstab Mount Definition**:
   Append a standard fstab-formatted line to `/home/user/fstab_entry.txt` (creating it if it doesn't exist) that mounts an NFS share `metrics-server:/var/log/metrics` to the local directory `/home/user/capacity_logs`. Use the `nfs` filesystem type, with the mount options exactly set to `ro,nosuid,nodev`. Default dump and pass numbers to `0`.

3. **SSH Tunneling Command**:
   Write a single SSH command into a text file at `/home/user/tunnel_cmd.txt`. This command should establish a local port forward (tunneling) from local port `9090` to the remote destination `internal-api.local:80`, routing through the bastion host `jump@gateway.corp.com`. The SSH command must include the flags to run in the background (`-f`) and not execute a remote command (`-N`). Do not execute the ssh command, just save it to the file.

Make sure your bash script is executable (`chmod +x /home/user/capacity_setup.sh`) and run it so the files are generated.