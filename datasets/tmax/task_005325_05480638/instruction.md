You are a penetration tester investigating a compromised host. You have discovered a compiled Python bytecode file at `/home/user/app.pyc` that acts as a beacon to a Command and Control (C2) server. You have also intercepted some raw HTTP traffic logs at `/home/user/traffic.log`.

Your objectives are:
1. **Reverse Engineering:** Disassemble the `/home/user/app.pyc` file using Python's built-in `dis` module. Identify the C2 server IP address and the custom authentication token used in the `X-Auth-Token` HTTP header.
2. **Traffic Inspection & Data Redaction:** Write a Python script `/home/user/process_traffic.py` to process `/home/user/traffic.log`. 
    - The log contains newline-separated JSON objects representing HTTP requests, with keys: `method`, `ip`, `headers` (dictionary), and `body`.
    - Find all POST requests destined for the C2 IP address that contain the correct `X-Auth-Token` header.
    - In the `body` of these requests, search for any US Social Security Numbers (format: `XXX-XX-XXXX` where X is a digit) and redact them by replacing the last four digits with `REDACTED` (e.g., `123-45-REDACTED`).
    - Save the redacted bodies, one per line, to `/home/user/redacted_payloads.txt`.
3. **Firewall Policy:** Create a shell script at `/home/user/block_c2.sh` containing a single `iptables` command to drop all outgoing traffic (OUTPUT chain) destined for the C2 IP address. Ensure the script is executable.

You must accomplish this without root access (do not run the iptables command, just write it to the file). Use Python for the traffic processing and redaction logic.