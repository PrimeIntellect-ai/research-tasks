You are a compliance analyst investigating a potential breach on a web server. The incident response team has isolated an unauthorized executable and an encrypted file left behind by the attacker. They are located at:
- `/home/user/evidence/telemetry_svc` (an ELF binary)
- `/home/user/evidence/audit_log.enc` (an encrypted data file)

Your objective is to perform forensic analysis, decrypt the compromised data, and prepare a network remediation script. 

**Step 1: Cryptanalysis & Decryption**
The attacker encrypted `/home/user/evidence/audit_log.enc` using a single-byte XOR cipher. Standard compliance logs on this system always begin with the exact 13-character string: `[AUDIT_START]`. 
Use this known-plaintext to deduce the XOR key, decrypt the entire contents of `audit_log.enc`, and save the resulting plaintext to exactly:
`/home/user/decrypted_audit.txt`

**Step 2: Binary Analysis & Firewall Policy**
Analyze the `/home/user/evidence/telemetry_svc` ELF binary. The attacker hardcoded a single IPv4 address into this binary, which is used as the exfiltration endpoint. Find this IP address.
Once you have identified the IP address, create a shell script at exactly:
`/home/user/remediation.sh`
This file must contain exactly one line: the `iptables` command required to drop all outbound TCP traffic to that specific IP address on port 443. 
You must use the exact following format for the command (replace `<IP>` with the extracted address):
`iptables -A OUTPUT -d <IP> -p tcp --dport 443 -j DROP`

Do not execute the iptables command (as you do not have root privileges); only write the precise command into the `remediation.sh` file.