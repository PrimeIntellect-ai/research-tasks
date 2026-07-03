You are an incident responder investigating a suspected local compromise on a developer machine. You have limited (non-root) access to the `/home/user` environment. The security team suspects a rogue background service is running on a high port, serving modified application files, and has a vulnerable authentication endpoint. 

Your objective is to investigate this environment using Bash scripting and standard Linux tools. Complete the following tasks:

1. **Service Auditing**: 
   Write a Bash script at `/home/user/audit_ports.sh` that scans the local TCP ports between 8000 and 8100 (inclusive) on `127.0.0.1`. The script should write only the port numbers of any actively listening services to `/home/user/active_ports.log` (one port per line). Execute this script.

2. **File Integrity Verification**:
   The primary web application files are located in `/home/user/app/public/`. A trusted baseline of SHA256 hashes is provided at `/home/user/baseline.sha256`. Use Bash commands to verify the integrity of the files in the directory against the baseline. 
   Write the absolute file paths of any files that fail the integrity check (modified files) to `/home/user/modified_files.txt` (one path per line).

3. **Authentication Flow Testing**:
   Using the active port you discovered in Task 1, write a Bash script at `/home/user/test_auth.sh` that tests the rogue service's authentication. The service exposes a POST endpoint at `http://127.0.0.1:<PORT>/admin`. 
   The script must send a POST request using `curl` with the JSON payload `{"username": "admin", "password": "password123"}` and the `Content-Type: application/json` header.
   The script should extract *only* the HTTP response status code (e.g., 200, 401, 403) and write it to `/home/user/auth_status.txt`. Execute this script.

4. **Network Policy Configuration (App-Level Firewall)**:
   The application uses a local IP blocklist file at `/home/user/app/acl.conf`. To simulate firewall remediation without root access, write a Bash script at `/home/user/block_ip.sh` that appends the exact string `deny 10.10.50.15` to the end of `/home/user/app/acl.conf`. Ensure the script makes the file read-only (`chmod 444`) after appending the rule. Execute this script.

Ensure all requested log files and scripts exist at their specified paths before you finish.