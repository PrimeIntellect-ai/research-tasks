You are a forensics analyst investigating a compromised Linux server. You have been provided with two artifacts recovered from the machine:

1. `/home/user/payload.b64`: A base64-encoded file containing a malicious TLS certificate dropped by the attacker to establish a reverse shell listener.
2. `/home/user/access.log`: An Nginx access log containing web traffic during the time of the compromise.

Your tasks are:
1. Decode the base64 payload to retrieve the TLS certificate. Extract the Subject Common Name (CN) of this certificate.
2. Analyze the `access.log` to identify successful SQL injection attacks. An attack is considered a successful SQL injection if:
   - The URL (after URL decoding) contains the string `UNION SELECT` or `' OR 1=1` (case-insensitive).
   - The HTTP response status code is `200`.
   Note: The log also contains XSS attempts and failed attacks (status `403` or `404`), which you must ignore.
3. Extract the source IP addresses of the successful SQL injection attacks.
4. Create a final report at `/home/user/forensics_report.txt` with the following format:

```text
CN: <extracted_common_name>
IPs: <comma_separated_list_of_ips_sorted_numerically>
```

Example of `forensics_report.txt` format:
```text
CN: fake-domain.com
IPs: 10.0.0.1,192.168.0.5
```

Write all necessary Bash scripts or commands to decode the payloads, parse the logs, and extract the required information.