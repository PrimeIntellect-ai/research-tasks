You are a compliance analyst investigating a potential credential leak. It is suspected that poorly written scripts are leaking encrypted authentication tokens via their command-line arguments, which are visible to system monitoring tools, and sending them to unauthorized external servers.

You have been provided with an audit log containing recent process executions and network connections at `/home/user/audit_events.log`. Each line in this file is a JSON object with the following fields:
- `pid`: Process ID
- `cmdline`: The full command-line string executed
- `dest_ip`: The destination IP address the process connected to

Your task is to identify and block the IP addresses receiving administrative tokens.

To do this, you must write a Python script to perform the following steps:
1. **Parse the Logs:** Read `/home/user/audit_events.log` and extract the hex-encoded payloads passed via the `--payload` argument in the `cmdline` field.
2. **Cryptanalysis:** The payloads are encrypted using a repeating-key XOR cipher. You know from the application's source code that the plaintext of every valid token starts with the exact string `AUTH_TOKEN:` (which is 11 bytes long). The XOR key used is exactly 4 bytes long, but different processes might use different keys. Using this known plaintext, recover the 4-byte key for each payload and decrypt the entire token.
3. **Correlation:** Check the decrypted plaintext of each token. If the plaintext contains the substring `ADMIN`, record the `dest_ip` associated with that process.
4. **Firewall Policy Generation:** Generate a bash script at `/home/user/apply_firewall.sh` that blocks outbound traffic to the identified malicious IP addresses. 

Requirements for `/home/user/apply_firewall.sh`:
- The first line must be exactly `#!/bin/bash`
- Subsequent lines must be valid iptables commands to drop traffic to the identified IPs: `iptables -A OUTPUT -d <IP> -j DROP`
- The `iptables` commands must be sorted numerically by the IP address (e.g., `10.1.2.3` comes before `172.16.0.10`).
- Ensure the script has execute permissions (`chmod +x`).

Write your script, execute it, and verify that `/home/user/apply_firewall.sh` is created with the correct format.