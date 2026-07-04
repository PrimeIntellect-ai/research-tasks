You are a penetration tester acting as a security consultant. During an audit of a staging environment, you have intercepted a log of HTTP traffic and noticed several security issues, including unencrypted sensitive headers and a misconfigured SSH daemon. 

You need to perform the following steps to analyze the data, redact sensitive information, and prepare remediation scripts.

**1. HTTP Traffic Inspection & Redaction**
You have been provided with an HTTP traffic log at `/home/user/traffic.json`. The file contains a JSON array of request objects. Each object has a `"source_ip"` and a `"headers"` dictionary.
Write a Python script at `/home/user/audit.py` that:
- Reads `/home/user/traffic.json`.
- Filters and retains ONLY the requests where the `"Cookie"` header contains the string `admin_session`.
- For these filtered requests, if an `"Authorization"` header exists, redact its value completely by replacing it with the exact string `[REDACTED]`.
- Outputs the filtered and redacted list of JSON objects to `/home/user/audit_results.json` (maintain the original structure, just a shorter list with redacted auth headers).

**2. Firewall Network Policy**
Identify the `"source_ip"` that made the highest number of requests containing the `admin_session` cookie in the original log. 
Create a shell script at `/home/user/block_ip.sh` containing exactly one `iptables` command to drop all incoming traffic from this specific IP address. Use the standard format: `iptables -A INPUT -s <IP_ADDRESS> -j DROP`.

**3. SSH Hardening**
You have a copy of the server's SSH configuration at `/home/user/sshd_config`.
Modify this file directly to harden it by ensuring the following two settings are configured correctly (uncommented and set to these values):
- `PermitRootLogin no`
- `PasswordAuthentication no`
If the settings exist but are commented out or set to `yes`, update them. If they do not exist, append them to the end of the file.

Ensure all scripts are executable and the final output files are correctly formatted. You do not need to execute the `block_ip.sh` script or restart SSH, just prepare the files.