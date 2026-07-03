You are a DevSecOps engineer tasked with implementing a "policy-as-code" enforcement tool. A recent security audit revealed that developers have accidentally uploaded SSH private keys to a public-facing web directory, and unauthorized IPs have been probing the web server for these files.

Your task is to write a Go program `/home/user/policy_enforcer.go` that automates incident response and enforces secure configurations. The tool must perform the following actions when compiled and executed:

1. **Log Parsing & Correlation:**
   - Parse the web server access log located at `/home/user/logs/access.log`. The log uses the standard Combined Log Format.
   - Identify all unique IP addresses that made HTTP `GET` requests for any file path containing the strings `.pem`, `.key`, or `id_rsa`. 
   - Collect these suspicious IPs.

2. **File Permission & Access Control (Quarantine):**
   - Recursively scan the web root directory `/home/user/web_app/public/` for any exposed private keys. A file is considered a private key if it contains the string `-----BEGIN ` followed by any characters, followed by ` PRIVATE KEY-----` (e.g., `-----BEGIN RSA PRIVATE KEY-----` or `-----BEGIN OPENSSH PRIVATE KEY-----`).
   - For every private key found:
     1. Change its file permissions to `0600`.
     2. Move it to the quarantine directory: `/home/user/quarantine/`. Keep the original filename.

3. **SSH Hardening Policy:**
   - Create a hardened SSH configuration snippet at `/home/user/sshd_config.snippet` containing exactly the following lines, enforcing our strict key-management and access policy:
     ```
     PermitRootLogin no
     PasswordAuthentication no
     X11Forwarding no
     MaxAuthTries 3
     ```

4. **Reporting:**
   - Generate a JSON report at `/home/user/security_report.json` summarizing the findings. The JSON must exactly match this structure:
     ```json
     {
       "suspicious_ips": ["<ip1>", "<ip2>"],
       "quarantined_files": ["<filename1>", "<filename2>"]
     }
     ```
   - Both the `suspicious_ips` array and `quarantined_files` array must be sorted in ascending alphabetical/lexicographical order.

**Execution Instructions:**
- Ensure all directories exist (`/home/user/quarantine` should be created if it doesn't exist).
- Write your Go code in `/home/user/policy_enforcer.go`.
- Compile it to `/home/user/policy_enforcer`.
- Run the compiled executable so that the report and snippet are generated, and the vulnerable files are quarantined.