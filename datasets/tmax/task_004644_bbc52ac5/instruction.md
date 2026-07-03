You are a compliance analyst generating audit trails for legacy systems. You have been tasked with analyzing an undocumented, compiled logging daemon named `/home/user/audit_agent` (an ELF binary) to ensure it complies with our new network and cryptographic standards. We have lost the source code for this binary, but we know it establishes a mutually authenticated TLS connection to a hardcoded IP address using an embedded client certificate.

Your objective is to extract the embedded network configuration and cryptographic materials from the binary and generate a standardized audit report.

Write a Python script at `/home/user/analyze_agent.py` that performs the following actions:
1. Opens and analyzes the `/home/user/audit_agent` ELF binary.
2. Extracts the embedded IPv4 address, which is prefixed in the binary's read-only data with the string `TARGET_IP=`.
3. Extracts the embedded X.509 certificate (in PEM format).
4. Parses the extracted certificate using a standard Python library (like `cryptography`) to determine the Subject's Common Name (CN) and the expiration date (Not After) formatted as `YYYY-MM-DD HH:MM:SS`.
5. Generates an `iptables` firewall rule that would block outbound traffic to the extracted IP address.
6. Writes the results to `/home/user/audit_trail.log` in the exact following format:

```
[AUDIT] Embedded IP: <extracted_ip>
[AUDIT] Cert Subject: <extracted_common_name>
[AUDIT] Cert Expiry: <YYYY-MM-DD HH:MM:SS>
[AUDIT] Block Command: iptables -A OUTPUT -d <extracted_ip> -j DROP
```

Ensure your Python script runs without errors and successfully creates the `/home/user/audit_trail.log` file with the correct data.