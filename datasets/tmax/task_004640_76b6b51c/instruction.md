You are acting as a network security engineer investigating a recent server compromise. You have been provided with an incident data package located in `/home/user/incident_data/`. Your goal is to analyze the provided logs, system dumps, and a suspicious binary to reconstruct the attacker's kill chain. 

You need to perform the following steps using bash utilities:

1. **Authentication Flow & Injection Analysis:** Inspect `/home/user/incident_data/auth_logs.txt`. Find the exact SQL injection payload the attacker used in the `username` field to bypass the authentication flow. 
2. **Binary Format Analysis:** The attacker left behind a compiled executable at `/home/user/incident_data/backdoor.elf`. Analyze this binary to extract the hidden Command and Control (C2) IPv4 address hardcoded within it.
3. **Privilege Escalation Auditing:** Review `/home/user/incident_data/suid_dump.txt`, which contains a list of files with the SUID bit set at the time of the incident. Identify the non-standard, custom binary that the attacker likely used to escalate privileges to root.
4. **Log Correlation:** Cross-reference the discovered C2 IP address with `/home/user/incident_data/network_traffic.log`. Find the exact timestamp of the *first* outgoing connection to this C2 server, representing the start of data exfiltration.

Write your final findings into a strict JSON file located at `/home/user/incident_report.json`. The JSON file must have exactly the following keys:
- `"sql_payload"`: The exact string of the SQL injection payload used in the username field.
- `"c2_ip"`: The IPv4 address of the C2 server extracted from the binary.
- `"privesc_binary"`: The absolute path of the vulnerable SUID binary.
- `"exfil_timestamp"`: The timestamp of the first connection to the C2 server (exactly as formatted in the network log).