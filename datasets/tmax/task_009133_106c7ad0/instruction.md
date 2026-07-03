You are an incident responder investigating a compromised Linux workstation. We suspect the attacker left a backdoor via a vulnerable local web service and escalated privileges by leaving misconfigured files in the system. 

You need to write a Go program at `/home/user/investigate.go` that automates the analysis of the service logs, decodes the attacker's payloads, generates a firewall remediation script, and audits a specific directory for privilege escalation vectors.

Your Go program must perform the following tasks:

1. **Payload Decoding and Pattern Matching (IDS):**
   - Read the log file located at `/home/user/service.log`.
   - Each line in the log file represents an HTTP GET request and contains a URL parameter `payload=` followed by a base64-encoded string.
   - Extract and decode the base64 string for each line.
   - Analyze the decoded string. We consider a payload malicious if it contains the command `wget` or `ncat`.
   - Extract the IPv4 address associated with the malicious command. The IP will immediately follow `http://` for `wget` (e.g., `wget http://1.2.3.4/file`) or immediately follow the command for `ncat` (e.g., `ncat 1.2.3.4 4444`).

2. **Firewall Policy Generation:**
   - For every unique malicious IP address discovered in step 1, generate a firewall rule to block it.
   - Write these rules to `/home/user/block.sh`.
   - The file should contain exactly one command per IP in the following format: `iptables -A INPUT -s <IP> -j DROP`
   - The commands in `/home/user/block.sh` must be sorted alphabetically by the IP address string.

3. **Privilege Escalation Auditing & File Permissions:**
   - Scan the directory `/home/user/suspicious_dir`.
   - Identify any files that are either:
     a) World-writable (the "others" write permission bit is set).
     b) Have the SUID (Set Owner User ID) bit set.
   - Write the base names (not the full paths) of these vulnerable files to `/home/user/vuln_files.txt`.
   - The file names in `/home/user/vuln_files.txt` must be sorted alphabetically, one per line.

Requirements:
- Your solution must be implemented entirely in `/home/user/investigate.go`.
- You can run the Go program to generate the required output files (`/home/user/block.sh` and `/home/user/vuln_files.txt`).
- Do not modify `/home/user/service.log` or the contents of `/home/user/suspicious_dir`.