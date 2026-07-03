You are acting as a compliance analyst tasked with generating an audit trail for a compromised internal server. The server's intercepted network traffic and SSH configuration have been dumped to your workspace.

You need to perform the following analysis:

1. **Traffic Analysis & Credential Recovery**:
   Inspect the intercepted HTTP traffic log at `/home/user/intercepted_traffic.txt`. Find the HTTP request and locate the `Session-Auth` cookie. The value of this cookie is a Base64-encoded JSON payload containing a compromised MD5 password hash. 
   Write a Python script to extract this hash and perform a dictionary attack using the wordlist provided at `/home/user/wordlist.txt` to find the plaintext password.

2. **SSH Configuration Audit**:
   Review the SSH daemon configuration file at `/home/user/sshd_config`. You need to identify which of the following critical security directives are currently set to insecure values:
   - `PermitRootLogin` (Secure value: `no`)
   - `PasswordAuthentication` (Secure value: `no`)
   - `X11Forwarding` (Secure value: `no`)
   If any of these directives are missing or set to anything other than their secure value, they should be flagged as insecure.

3. **Audit Report Generation**:
   Generate an audit report in JSON format and save it strictly to `/home/user/audit_report.json`. The JSON file must have exactly the following structure:
   ```json
   {
     "compromised_password": "<plaintext_password>",
     "insecure_ssh_directives": [
       "<Directive1>",
       "<Directive2>"
     ]
   }
   ```
   The `insecure_ssh_directives` list should contain the exact names of the directives (from the 3 listed above) that are insecurely configured in the `sshd_config` file, sorted in alphabetical order.

Complete this task by saving the final `audit_report.json` file in `/home/user/`.