You are a security engineer tasked with rotating credentials and securing the environment for a legacy internal application. You must perform a credential rotation, audit and patch a privilege escalation vulnerability, and tighten the application's firewall policy.

You have been provided with the following environment (assume these files exist in your workspace):
1. **Configuration File**: `/home/user/legacy_app/config.ini`
2. **Encoding Tool**: `/home/user/legacy_app/encode_pass.sh`
3. **Firewall Rules Backup**: `/home/user/firewall/iptables.rules`
4. **Sudoers Snippet**: `/home/user/audit/sudoers_app`

Perform the following tasks using standard Linux command-line tools:

**Step 1: Credential Rotation (Cryptographic Encoding)**
The database password in `/home/user/legacy_app/config.ini` is stored in a custom encoded format. 
You must rotate the password to exactly: `SuperSecretRotate2024!`
Use the provided script `/home/user/legacy_app/encode_pass.sh` to encode this new password. Update the `DB_PASS` value in `config.ini` with the newly encoded string. Do not alter other lines in the file.

**Step 2: Privilege Escalation Auditing**
The service account `app_user` has a dedicated sudoers file at `/home/user/audit/sudoers_app`. It currently contains a misconfiguration that allows trivial privilege escalation to root. 
Edit `/home/user/audit/sudoers_app` to remove ONLY the binary that allows interactive shell escape (e.g., `/bin/bash`, `/bin/sh`, etc.) from the `NOPASSWD` list. Leave the legitimate service restart script (`/usr/bin/systemctl restart legacy_app`) intact.

**Step 3: Firewall Policy Configuration**
The application's firewall backup file `/home/user/firewall/iptables.rules` currently allows inbound TCP connections to the application port (port 8080) from anywhere (`0.0.0.0/0`).
Modify `/home/user/firewall/iptables.rules` so that port 8080 is ONLY accessible from the specific internal IP `10.50.100.5`. Replace `0.0.0.0/0` with `10.50.100.5` on the relevant port 8080 rule.

**Step 4: Audit Log**
Create a verification log at `/home/user/rotation_log.txt` with the following three lines:
Line 1: The new encoded password string.
Line 2: The exact modified rule line from `iptables.rules`.
Line 3: The exact modified sudoers line from `sudoers_app`.