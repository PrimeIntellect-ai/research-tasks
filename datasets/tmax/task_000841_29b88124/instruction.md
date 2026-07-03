You are a DevSecOps engineer responsible for enforcing security policy as code. You have a legacy application located in `/home/user/vulnerable_app` that needs an automated security audit.

Your task is to write a Go program located at `/home/user/sec-audit.go` that performs four specific security policy checks on the application's source code and configuration. Once written, compile and run your Go program to generate the required audit reports and remediation scripts.

The Go program must perform the following actions:

1. **Privilege Escalation Auditing**:
   Read `/home/user/vulnerable_app/rbac.json`. This file contains an array of roles. Find any role where `can_sudo` is `true` but the role `name` is NOT exactly `"admin"`. Write the names of these non-admin privileged roles to `/home/user/privesc.log`, one per line.

2. **Injection and XSS Vulnerability Analysis**:
   Scan all `.go` and `.html` files in `/home/user/vulnerable_app` and its subdirectories.
   - If a `.go` file contains the exact substring `fmt.Sprintf("SELECT`, it represents an SQL injection risk. Write the full absolute path of the file to `/home/user/injection.log`, one per line.
   - If a `.html` file contains the exact substring `{{.`, it represents a potential XSS risk due to unescaped Go templates. Write the full absolute path of the file to `/home/user/xss.log`, one per line.

3. **Sensitive Data Redaction**:
   Read the configuration file at `/home/user/vulnerable_app/secrets.txt`. Search for any AWS access keys, which for this task are defined as any string of non-whitespace characters starting exactly with `AKIA`. Replace these keys with the exact string `[REDACTED]`. Save the sanitized file to `/home/user/secrets_clean.txt`.

4. **Firewall and Network Policy Configuration**:
   Read the threat intelligence feed at `/home/user/vulnerable_app/threats.txt`, which contains a list of malicious IP addresses (one per line). Generate a bash script at `/home/user/block.sh` that appends rules to block these IPs. The file must start with `#!/bin/bash` on the first line. For each IP, add a line: `iptables -A INPUT -s <IP_ADDRESS> -j DROP`. Set the executable permission (`0755`) on `/home/user/block.sh`.

Ensure your Go program handles the file parsing and output generation accurately. Run your Go program to produce the final log files and scripts before finishing the task.