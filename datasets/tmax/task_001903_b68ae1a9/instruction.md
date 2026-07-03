You are a security engineer responsible for credential rotation and incident response. A recent audit revealed that a legacy application has been inadvertently logging sensitive credentials (passwords and API keys) in plain text during rotation requests. Additionally, we need to immediately block the IP addresses that submitted these exposed requests, as they may be compromised or belong to unauthorized scanners.

Your task is to write a Go program located at `/home/user/sec_tool.go` that performs automated scanning, data redaction, and firewall policy generation based on an existing log file.

**Requirements:**
1. **Automated Scanning & Sensitive Data Redaction:**
   Read the log file located at `/home/user/app.log`. Scan each line for leaked credentials. Credentials appear in the format `PASSWORD=<alphanumeric_string>` or `API_KEY=<alphanumeric_string>`. 
   You must redact the actual values by replacing them exactly with `***` (e.g., `PASSWORD=***` or `API_KEY=***`).
   Write the fully redacted log to `/home/user/app_redacted.log`, preserving the original order and formatting of the lines, except for the redacted values.

2. **Firewall and Network Policy Configuration:**
   Identify the IP addresses associated with the log lines where a credential was exposed. The IP address in the log line is specified in the format `IP=<ipv4_address>`.
   For every unique IP address that submitted a request containing a leaked credential, generate a firewall rule to drop traffic from that IP.
   The output format must be standard iptables commands: `iptables -A INPUT -s <IP> -j DROP`.
   Write these commands, one per line, to `/home/user/block_ips.sh`. If an IP appears multiple times with exposed credentials, only output the iptables command for it once.

**Execution:**
Once your Go script is written, run it to generate `/home/user/app_redacted.log` and `/home/user/block_ips.sh`. 

Ensure both output files exactly match the specifications, as automated systems will parse them for verification.