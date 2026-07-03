You are a Linux systems engineer performing routine hardening on a simulated environment. You have been provided with a vulnerability report and need to remediate several filesystem, configuration, and network issues.

Please perform the following steps:

1. **Parse Vulnerability Report & Generate Firewall Script:**
   Read the file `/home/user/vulnerability_scan.txt`. Find all lines that exactly match the pattern: 
   `CRITICAL: Unauthorized listener on TCP port <PORT>` (where `<PORT>` is a number).
   Extract these port numbers and create a bash script at `/home/user/apply_fw.sh`. 
   The script must:
   - Begin with `#!/bin/bash`
   - Contain the command `iptables -I INPUT -p tcp --dport <PORT> -j DROP` for each unique extracted port.
   - The `iptables` commands must be sorted by the port number in ascending numerical order.
   - The script file must be made executable.

2. **Environment Configuration:**
   Append the environment variable `export SEC_HARDENED=true` to the end of the `/home/user/.bashrc` file.

3. **Filesystem Quarantine:**
   You must quarantine insecure application configurations. Search through the directory `/home/user/app_data/` and all of its subdirectories for files ending in `.conf`.
   If a `.conf` file contains the exact string `ALLOW_ANON` anywhere in its contents:
   - Create the directory `/home/user/quarantine/` (if it doesn't already exist).
   - Move the vulnerable file into `/home/user/quarantine/`.
   - Change the moved file's permissions to `000` (no read, write, or execute permissions for owner, group, or others).

Ensure all file paths are absolute and exactly match the instructions.