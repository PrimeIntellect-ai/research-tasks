You are a DevSecOps engineer enforcing security policy as code. You need to automate the auditing of a simulated web server environment. 

We have simulated an environment in `/home/user/` with the following components:
1. `/home/user/access.log`: A web server log file. The server has a login endpoint `/login?redirect=`. The `redirect` parameter receives a Base64 encoded URL. 
2. `/home/user/deploy_scripts/`: A directory containing deployment scripts.
3. `/home/user/open_ports.txt`: A file listing currently active port numbers on the server, one per line.

Your task is to write a Bash script at `/home/user/policy_audit.sh` that performs the following security data processing and auditing tasks:

1. **Payload Decoding and Open Redirect Analysis**:
   Parse `/home/user/access.log`. Extract the IP addresses of users who successfully exploited an open redirect. A payload is considered an open redirect exploit if the Base64 decoded URL starts with `http://` or `https://` AND the domain is NOT `localhost` or `127.0.0.1`. (Ignore relative paths that just start with `/`).
   
2. **Privilege Escalation Auditing**:
   Scan the directory `/home/user/deploy_scripts/` for any files that are world-writable (permissions allow anyone to write). This violates our secure configuration policy.

3. **Service Auditing**:
   Read `/home/user/open_ports.txt`. Our policy states that only ports `80` and `443` are authorized. Any other port is considered unauthorized.

Your script `/home/user/policy_audit.sh` must execute without any arguments and generate a report file at `/home/user/audit_results.txt` with exactly the following format:

```
OPEN_REDIRECT_IPS: <comma-separated list of IPs sorted in ascending order>
PRIVESC_VULN_FILES: <comma-separated list of world-writable file names (just the basenames, e.g., script.sh) sorted in ascending order>
UNAUTHORIZED_PORTS: <comma-separated list of unauthorized port numbers sorted in ascending numerical order>
```

Constraints:
- You must write the solution using only standard Bash built-ins, coreutils, and standard CLI tools (e.g., `awk`, `grep`, `sed`, `base64`, `find`).
- Do not use Python, Perl, or other scripting languages.
- Ensure your script is executable (`chmod +x /home/user/policy_audit.sh`).
- If no items are found for a category, leave the value empty after the colon and space (e.g., `OPEN_REDIRECT_IPS: `).