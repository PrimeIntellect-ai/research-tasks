You are acting as a security auditor performing a security assessment on an internal server. I need your help to audit the SSH configuration, check the permissions of SSH keys, and test a custom authentication flow using a Python service.

Please perform the following tasks:

1. **SSH Configuration Audit:**
   An SSH configuration file is located at `/home/user/audit/sshd_config`. Audit this file for two specific weak settings:
   - Root login is permitted.
   - Password authentication is enabled.
   Create a file named `/home/user/ssh_audit.log`. For every weak setting found from the two mentioned above, write a line in the format: `FAILED: <DirectiveName>` (e.g., `FAILED: PermitRootLogin` or `FAILED: PasswordAuthentication`).

2. **Key Permission Audit:**
   There is a directory of SSH keys located at `/home/user/audit/keys/`. As an auditor checking permissions, you must identify any private keys (files starting with `id_rsa`) that are "world-readable" (i.e., others have read permission). 
   Write the absolute file paths of any vulnerable keys to a file named `/home/user/vuln_keys.log`, with one path per line.

3. **Authentication Flow Testing:**
   There is a local Python authentication script at `/home/user/audit/auth_service.py`. This script reads a base64-encoded JSON payload from a file. 
   Review the logic of `auth_service.py`. Your goal is to craft a valid payload that successfully authenticates as the user "auditor" with the role "admin", bypassing the intended normal user flow. 
   Generate this base64-encoded JSON payload and save it to `/home/user/payload.txt`.

Ensure all log files and payload files are created exactly as requested in the `/home/user/` directory.