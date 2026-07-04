You are an observability engineer tasked with configuring the local development environment for managing dashboard deployments and establishing secure access to the internal observability API. You must complete three interconnected configuration tasks without requiring root privileges.

**Task 1: Dashboard Repository Git Hook**
We use a local bare Git repository at `/home/user/dashboards.git` to store dashboard JSON configurations.
Create a `pre-receive` hook for this repository. The hook must be written in Bash or Python and be executable. 
It must intercept pushes and check the content of any newly pushed or modified files ending in `.json`.
If any of these modified/new `.json` files contain the exact string `"uid": null`, the hook must:
1. Reject the push (exit with a non-zero status).
2. Print exactly this string to standard error: `Observability Policy Violation: Null UID found.`

**Task 2: Simulated File System Mount Configuration**
We mount a dedicated volume for dashboard backups. Since you lack root access to modify `/etc/fstab`, we use a custom user-level config file.
Create a file at `/home/user/dashboard_fstab`. Add a standard fstab-formatted line to mount a block device with the UUID `9a3b2c1d-8e7f-4a5b-6c7d-8e9f0a1b2c3d` to the mount point `/home/user/dashboards_backup`. 
The filesystem type must be `ext4`. The mount options must be exactly `rw,nosuid,nodev,noexec`. The dump frequency must be `0` and the fsck pass number must be `2`. 

**Task 3: SSH Port Forwarding & Authentication Configuration**
You need to establish a local port forward to the internal dashboard API via a jumpbox, while strictly disabling key-based authentication (to enforce compliance with a specific password-based rotation policy).
Create or modify the SSH client configuration file at `/home/user/.ssh/config`.
Add a configuration for the host `obs-jumpbox` with the following requirements:
- Real hostname/IP: `192.168.10.100`
- User: `o11y`
- Port: `2222`
- Map local port `8080` to `dashboard-api.internal:80` on the remote side.
- Silently reject key-based login by explicitly disabling public key authentication and explicitly enabling password authentication.

Ensure all files have the appropriate permissions and are located in the exact paths specified.