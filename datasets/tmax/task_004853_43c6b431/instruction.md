You are a DevSecOps engineer responsible for enforcing Security Policy as Code. You have been provided with an offline dataset of logs, network policies, and connection attempts. Your task is to write a Python script that processes these files, verifies their integrity, inspects HTTP/Auth data, and evaluates network policies.

The files are located in `/home/user/sec_data/`:
1. `auth_logs.json`: Contains a JSON array of simulated HTTP request/response logs.
2. `network_policy.json`: Defines the ingress firewall rules as JSON.
3. `connections.csv`: A list of network connection attempts to evaluate.
4. `manifest.sha256`: A standard SHA256 checksum file for the three files above.

Write a Python script at `/home/user/audit.py` that performs the following steps and outputs the results to `/home/user/audit_report.json`.

**Step 1: File Integrity Verification**
Calculate the SHA256 hash of `auth_logs.json`, `network_policy.json`, and `connections.csv`. Compare them to the hashes in `manifest.sha256`. 
In your output report, record the status as `"PASS"` or `"FAIL"` for each file.

**Step 2: HTTP Header & Authentication Inspection**
Parse `auth_logs.json`. Each entry has an `"id"`, a `"request"` object, and a `"response"` object.
An entry is considered to have an **Auth Violation** if ANY of the following are true:
- The request contains an `"Authorization"` header, but it does NOT start with `"Bearer "`.
- The response contains a `"Set-Cookie"` header, but it is missing the `"Secure"` directive (case-sensitive, exact match of the word `Secure` separated by semicolons/spaces) OR missing the `"HttpOnly"` directive.

Record the IDs of all logs that have violations.

**Step 3: Network Policy Evaluation**
Parse `network_policy.json`. It contains a list of allowed rules (e.g., `[{"src_ip_range": "192.168.1.0/24", "dest_port": 443}, ...]`). The default policy is DENY.
Parse `connections.csv`, which has headers `conn_id,src_ip,dest_port`.
For each connection, determine if it is `"ALLOWED"` or `"DENIED"`. A connection is ALLOWED if its `src_ip` falls within any of the CIDR blocks in the policy AND the `dest_port` matches the rule's port. Otherwise, it is DENIED. (You may use Python's built-in `ipaddress` module).

**Output Format**
Your script must generate `/home/user/audit_report.json` with the exact following structure:
```json
{
  "integrity_checks": {
    "auth_logs.json": "PASS",
    "network_policy.json": "PASS",
    "connections.csv": "PASS"
  },
  "auth_violations": [1, 3, 4],
  "connection_evaluations": {
    "c1": "ALLOWED",
    "c2": "DENIED"
  }
}
```
*(The arrays and objects should contain your actual computed results).*

Ensure your script runs successfully and creates the exact output file required. You can use standard Python 3 libraries.