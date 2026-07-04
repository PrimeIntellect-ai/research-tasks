You are an AI assistant helping a network engineer troubleshoot a diagnostic backup system running on a local Linux machine.

The system is supposed to securely fetch running configurations from a local test router (simulated via localhost SSH) and back them up to a mounted directory. However, the automated backup system is failing due to SSH misconfigurations, and the backup logic needs to be rewritten.

You need to complete the following tasks:

1. **Fix SSH Connectivity:**
   The network engineer uses an SSH alias `router-01` to connect to the local test environment. Running `ssh router-01 cat /home/user/router_config.txt` currently fails because the SSH key-based login is silently failing or being rejected by the SSH client due to bad security practices. 
   Identify the problem with the SSH configuration or keys located in `/home/user/.ssh/` and fix it so that `ssh router-01` can authenticate successfully without a password. Do not change the key pair itself, just fix the permissions or configurations.

2. **Mount Point Resolution:**
   The engineer has a custom fstab file at `/home/user/network_fstab` that keeps track of simulated mount points. 
   Find the mount point path associated with the device `//storage-node/router-backups` in this file. 
   Create this target directory on the local file system (e.g., `/home/user/something...`).

3. **Develop the Interactive Backup Manager (Python):**
   Write an interactive Python script at `/home/user/net_manager.py`. The script must read commands from standard input (`stdin`) in a loop.
   - When it receives the string `BACKUP`, it should execute an SSH command to fetch the contents of `/home/user/router_config.txt` from `router-01`. It must then save this exact content to a file named `router-01-latest.bak` inside the mount directory you identified in step 2. After successfully backing up, print `BACKUP_SUCCESS` to stdout.
   - When it receives the string `EXIT`, it should gracefully exit with a return code of 0.
   - For any other input, it should print `UNKNOWN_COMMAND` and continue running.

Ensure your Python script relies on the repaired SSH configuration to work securely and without interactive password prompts. Ensure the script handles newline characters from stdin properly.

**Initial System State that you can assume exists:**
- A public/private key pair in `/home/user/.ssh/` (`id_rsa`, `id_rsa.pub`).
- An SSH config file at `/home/user/.ssh/config` mapping `router-01` to `127.0.0.1`.
- The file `/home/user/router_config.txt` containing the mock router configuration.
- The file `/home/user/network_fstab`.
- The user's public key is already in `/home/user/.ssh/authorized_keys`.