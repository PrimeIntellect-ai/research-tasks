You are a network engineer and security analyst responding to a suspicious network event. You have intercepted traffic and artifacts related to a potential compromise. Your goal is to process the intercepted data, analyze the malicious payload for vulnerabilities, extract Command and Control (C2) infrastructure details from a certificate, and generate a firewall blocklist.

You have been provided with a directory `/home/user/incident_data/` containing:
1. `intercepted_payload.txt`: A multi-layer encoded payload extracted from the traffic.
2. `c2_certificate.pem`: A PEM-formatted X.509 certificate used by the C2 server for TLS communication.
3. `local_dns.json`: A JSON file mapping known internal and external domains to IP addresses.

Perform the following tasks and output your results in the `/home/user/analysis/` directory (you must create this directory):

**Phase 1: Payload Decoding**
The file `intercepted_payload.txt` contains data that has been compressed using `gzip`, and then the resulting binary data was Base64 encoded.
1. Decode the Base64 string.
2. Decompress the resulting binary data using `gzip`.
3. The result is a cleartext Python script. Save this script exactly as it is to `/home/user/analysis/malware.py`.

**Phase 2: Code Auditing (CWE Identification)**
Analyze the decoded Python script (`malware.py`). The script contains a highly specific vulnerability in how it handles system commands.
1. Identify the Common Weakness Enumeration (CWE) identifier for this exact vulnerability (e.g., CWE-22, CWE-79).
2. Write the CWE identifier (just the ID, e.g., "CWE-123") to `/home/user/analysis/cwe.txt`.

**Phase 3: Certificate Parsing**
1. Parse the `c2_certificate.pem` file.
2. Extract the Common Name (CN) from the Subject of the certificate.
3. Look up this CN in the `/home/user/incident_data/local_dns.json` file to find its corresponding IP address.
4. Write a single line containing the CN and the IP address, separated by a comma (e.g., `example.com,10.0.0.1`), to `/home/user/analysis/c2_info.txt`.

**Phase 4: Firewall Configuration**
Write a Python script at `/home/user/generate_fw.py` that dynamically reads `/home/user/analysis/c2_info.txt` and generates an iptables firewall rule to block all outbound traffic to the C2 IP address.
1. Run your script to generate the rule.
2. Save the exact generated rule to `/home/user/analysis/firewall.rules`. The file should contain exactly one line in this format: `iptables -A OUTPUT -d <IP_ADDRESS> -j DROP`.

Ensure all file paths and formatting strictly match the instructions, as your response will be verified by an automated system.