You are a network security engineer responding to an alert about anomalous traffic being dropped by the local firewall. You need to investigate the firewall logs, correlate the traffic with the local web services, verify the integrity of the services, and identify any injected vulnerabilities.

Your environment contains the following:
1. `/home/user/ufw.log`: A firewall log file containing dropped packet events.
2. `/home/user/web_services/`: A directory containing several Python microservices (`auth_service.py`, `data_service.py`, `proxy_service.py`). Each service binds to a specific port defined in its code.
3. `/home/user/hashes.txt`: A file containing the known-good SHA256 hashes of the Python microservices before deployment.

Perform the following investigation:
1. Analyze `/home/user/ufw.log` to determine which destination port (`DPT`) is receiving the highest number of dropped packets.
2. Identify which Python service in `/home/user/web_services/` is configured to run on that targeted port.
3. Verify the file integrity of all Python scripts in the `/home/user/web_services/` directory using `/home/user/hashes.txt`. Determine which file has been tampered with (its hash will not match).
4. Audit the source code of the tampered Python file to identify the specific vulnerability that was injected by the attacker. Determine the standard CWE ID (e.g., CWE-89, CWE-79, CWE-78) that best categorizes this vulnerability.

Finally, generate an investigation report at `/home/user/report.json` with exactly the following JSON structure:
```json
{
  "targeted_port": <integer>,
  "compromised_file": "<string, filename only>",
  "cwe_id": "<string, uppercase, e.g., 'CWE-123'>"
}
```

Ensure the file `/home/user/report.json` contains valid JSON. Do not include extra text in the file.