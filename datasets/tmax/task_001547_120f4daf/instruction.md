You are a compliance analyst performing a security audit on a legacy web server. We have detected that the server's login endpoint (`/login`) is vulnerable to an open redirect, and worst of all, it has been logging credentials in plaintext!

You have been provided with the raw access log file at `/home/user/server.log`.

Your objectives are to clean up the logs for compliance, identify the attackers, and generate a firewall script to block them. 

Please perform the following tasks:

1. **Sensitive Data Redaction**:
   Create a new log file at `/home/user/compliance_clean.log` based on `/home/user/server.log`. You must redact all plaintext passwords. Specifically, look for the `password=` query parameter in the URL of the log lines. Replace the actual password value with `[REDACTED]`. The rest of the log line must remain exactly the same.
   *Example:* `GET /login?user=admin&password=secret123&redirect_url=/home` should become `GET /login?user=admin&password=[REDACTED]&redirect_url=/home`

2. **Authentication Flow & Open Redirect Analysis**:
   Analyze the logs to find IP addresses that have exploited the open redirect vulnerability. An exploit is defined as any request where the `redirect_url` query parameter starts with `http://` or `https://` but does NOT target our internal domain `internal.company.local`. (Relative paths like `/dashboard` are safe).

3. **Firewall Policy Configuration**:
   Create a bash script at `/home/user/firewall_block.sh` to block the malicious IP addresses identified in Step 2.
   The script should contain exactly one line per unique malicious IP, in this exact format:
   `iptables -A INPUT -s <IP_ADDRESS> -j DROP`
   Sort the `iptables` commands by IP address in ascending alphabetical order. Add `#!/bin/bash` at the top of the script. Make sure the script is executable.

You may use Python, Bash, or any standard Linux utilities to accomplish this.