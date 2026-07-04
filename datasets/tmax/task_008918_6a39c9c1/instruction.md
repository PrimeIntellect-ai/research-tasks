You are a network security engineer investigating a potential breach. You have intercepted a custom application traffic log saved at `/home/user/traffic.log`. The log contains sensitive user data that needs to be redacted, as well as malicious, encrypted C2 (Command and Control) traffic from a known threat actor.

Your task is to write a C program to process this log, and then execute follow-up system commands to secure the environment.

**Step 1: Write a C program to process the log**
Write and execute a C program that reads `/home/user/traffic.log` line by line and performs the following operations:
1. **Security Log Parsing**: Read the custom format `[TIMESTAMP] [SOURCE_IP] [DEST_IP] PAYLOAD`.
2. **Sensitive Data Redaction**: The PAYLOAD sometimes contains Social Security Numbers in the format `SSN:123456789` (exactly 9 digits after `SSN:`). You must replace the digits so the output becomes `SSN:XXX-XX-XXXX`.
3. **Decryption**: Traffic originating from the malicious IP `[192.168.1.100]` contains an encrypted payload. The payload is a hex-encoded string. Your C program must hex-decode the string into bytes, and then decrypt it using a single-byte XOR key of `0x5A`. In the output log, replace the original hex payload with `DECRYPTED: <decrypted_string>`.
4. The C program must write the fully processed log to a new file at `/home/user/clean_traffic.log` keeping the exact same line structure and spacing, just with the PAYLOAD section modified as described above.

**Step 2: File Integrity Verification**
Once `/home/user/clean_traffic.log` is generated, compute its SHA-256 hash and save the standard output of the `sha256sum` command to `/home/user/clean_traffic.sha256`.

**Step 3: Firewall Configuration**
The decrypted payload from the malicious IP reveals a hidden C2 server IP address in the format `C2: <IP>`.
Create an executable bash script at `/home/user/block_c2.sh` that contains a shebang (`#!/bin/bash`) and exactly one `iptables` command to drop all outbound traffic to that newly discovered C2 IP address. Use the format: `iptables -A OUTPUT -d <C2_IP> -j DROP`.

Make sure `/home/user/block_c2.sh` has executable permissions.