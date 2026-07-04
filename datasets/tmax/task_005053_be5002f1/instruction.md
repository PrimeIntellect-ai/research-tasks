You are acting as a DevSecOps engineer. We need to implement a "Policy as Code" compliance check for a simulated environment. 

You have been provided with an audit data directory at `/home/user/audit_env`. This directory contains extracts of system logs, configuration files, and network state. Your task is to write a script (in Python, Bash, or any combination of tools) that analyzes this data and generates a JSON compliance report.

Here are the specific compliance rules you need to enforce:

1. **Security Log Parsing (Brute Force Detection):**
   - Parse the log file located at `/home/user/audit_env/logs/auth.log`.
   - Identify any IP address that has **more than 3** "Failed password" attempts for the user `admin`.
   - Collect these IP addresses into a list.

2. **Privilege Escalation Auditing:**
   - Parse the mock sudoers file located at `/home/user/audit_env/config/sudoers`.
   - Identify any user accounts (excluding `root`) that have been granted unrestricted passwordless sudo access. Specifically, look for lines matching the pattern where a user is granted `NOPASSWD: ALL` (e.g., `username ALL=(ALL) NOPASSWD: ALL` or similar variations with spacing).
   - Collect these usernames into a list.

3. **Service Auditing (Port Analysis):**
   - Parse the JSON file `/home/user/audit_env/network/ports.json`, which contains an array of objects representing scanned ports (e.g., `{"port": 22, "state": "open", "service": "ssh"}`).
   - The only explicitly authorized open ports in our policy are `22`, `80`, and `443`.
   - Identify any port numbers that have a state of `"open"` but are **not** in the authorized list.
   - Collect these unauthorized open port numbers into a list of integers.

**Expected Output:**
Your script must output the final results to exactly `/home/user/compliance_report.json`. The JSON file must have the following exact schema (arrays can be in any order, but the keys must match exactly):

```json
{
  "brute_force_ips": [
    "192.168.x.x"
  ],
  "unauthorized_sudo_users": [
    "user1",
    "user2"
  ],
  "unauthorized_open_ports": [
    1234,
    5678
  ]
}
```

Ensure your script extracts the data dynamically from the provided files, as the actual file contents will vary in the automated test. Run your script to generate the final `/home/user/compliance_report.json` file.