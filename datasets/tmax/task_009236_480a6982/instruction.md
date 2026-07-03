You are an infrastructure engineer automating the provisioning and deployment of a custom Go-based logging daemon. You need to set up a staged deployment, configure a custom `fstab`-like configuration for the app to resolve its log directories, and set up user-space log rotation.

Complete the following steps:

1. **Go Code Modification & Staged Deployment:**
You have a workspace at `/home/user/workspace/` containing a Go program `main.go` (you must create this). 
The Go program should:
- Read a configuration file passed as the first CLI argument. The file is formatted exactly like `/etc/fstab`.
- Find the line that starts with `UUID=APP_LOGS`.
- Extract the mount point (the second column) from that line.
- Write the string "DEPLOYMENT_V2_SUCCESS" to a file named `daemon.log` inside that extracted mount point directory.

Compile this Go program and deploy it using a staged directory structure:
- Create `/home/user/deploy/releases/v2/` and place the compiled binary there named `logdaemon`.
- Create a symlink at `/home/user/deploy/current` pointing to `/home/user/deploy/releases/v2`.

2. **Fstab Configuration:**
Create a mock fstab file at `/home/user/deploy/config/fstab.conf`. It must contain the following line (fields separated by tabs or spaces):
`UUID=APP_LOGS /home/user/deploy/logs ext4 defaults 0 2`
Make sure the `/home/user/deploy/logs` directory exists.

3. **Log Rotation Setup:**
Create a logrotate configuration file at `/home/user/deploy/config/logrotate.conf` that manages `/home/user/deploy/logs/daemon.log`.
It must specify:
- Rotation size of 10 bytes (`size 10`)
- Keep 3 backups (`rotate 3`)
- Compress old log files (`compress`)
- Missing logs are ok (`missingok`)

4. **Execution & Verification:**
- Run your deployed binary via the symlink: `/home/user/deploy/current/logdaemon /home/user/deploy/config/fstab.conf`
- Append 50 bytes of dummy text (e.g., "0123456789" repeated) to `/home/user/deploy/logs/daemon.log` to exceed the logrotate size threshold.
- Run the logrotate utility in user-space using your config: `logrotate -s /home/user/deploy/config/logrotate.state /home/user/deploy/config/logrotate.conf`

Ensure all files, symlinks, and rotated logs are perfectly in place at the end of your process.