You are a network security engineer tasked with inspecting captured traffic logs and remediating compromised endpoints. Your goal is to write a C++ program for intrusion detection (pattern matching), and a Bash script to audit TLS certificates and harden SSH access based on the findings.

**Step 1: Intrusion Detection (C++)**
You have been provided with two files:
1. `/home/user/traffic.log`: A log of network streams. Each line is formatted as: `<Timestamp> <Source_IP> <Target_Port> <Payload_String>`
2. `/home/user/signatures.txt`: A list of malicious payload signatures (one per line).

Write a C++ program at `/home/user/ids_matcher.cpp` that reads both files. If a `Payload_String` contains *any* of the exact substrings from `signatures.txt`, the `Source_IP` should be flagged. 
Compile your program using `g++ -std=c++17 /home/user/ids_matcher.cpp -o /home/user/ids_matcher` and execute it. 
Your program must output a file at `/home/user/flagged_ips.txt` containing only the unique flagged IP addresses, one per line.

**Step 2: Certificate Vulnerability Scanning (Bash)**
There is a directory `/home/user/certs/` containing several x509 PEM certificates used by various internal services. 
Create a bash script at `/home/user/secure_env.sh`. The script must inspect every `.pem` file in `/home/user/certs/`. It should find any certificates that are either:
- Expired (not valid as of the current system time), OR
- Using an RSA public key smaller than 2048 bits.

The script must write the absolute paths of these vulnerable/expired certificates to `/home/user/weak_certs.txt` (one path per line).

**Step 3: SSH Hardening (Bash)**
Your script `/home/user/secure_env.sh` must also secure the local SSH authorized keys. 
Read the IPs from `/home/user/flagged_ips.txt`. Look through the file `/home/user/.ssh/authorized_keys`. Remove any public key entry where the trailing comment exactly matches an IP address found in `flagged_ips.txt` (e.g., `ssh-rsa AAA... user@192.168.1.100` where `192.168.1.100` is flagged). Overwrite `/home/user/.ssh/authorized_keys` with the cleaned, safe entries.

Run your `/home/user/secure_env.sh` script to perform the remediation.