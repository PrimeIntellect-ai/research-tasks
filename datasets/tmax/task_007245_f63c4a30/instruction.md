You are acting as a network security engineer investigating a recent web server compromise. 

You have been provided with a custom application traffic log located at `/home/user/traffic.log`. 
Initial analysis suggests an attacker performed a brute-force attack against the login API, successfully guessed the administrator's password, and subsequently ran an automated vulnerability scanner to find and exploit a Local File Inclusion (LFI) vulnerability.

The log file format is:
`[Timestamp] IP_Address HTTP_Method URL Request_Body HTTP_Status`
*(Note: Request_Body is `-` for GET requests. For POST requests to `/api/login`, it contains a JSON payload).*

Your task is to write a Python script that parses `/home/user/traffic.log` to determine:
1. The IP address of the attacker.
2. The successfully brute-forced password for the user "admin".
3. The exact LFI payload (the value of the `file=` parameter) that successfully returned a 200 HTTP status code.

You must output your findings in a strictly formatted JSON file at `/home/user/incident_report.json`. 

The JSON must have the following exact structure and keys:
```json
{
  "attacker_ip": "<extracted_ip>",
  "compromised_password": "<extracted_password>",
  "successful_lfi_payload": "<extracted_payload>"
}
```

Constraints:
- You must use Python to solve this task.
- A successful login is indicated by a 200 HTTP status code on the `/api/login` endpoint.
- A successful LFI is indicated by a 200 HTTP status code on a URL containing directory traversal sequences (e.g., `../`).
- The log file contains background noise from legitimate users; only one IP performed both the brute-force and the LFI scan.