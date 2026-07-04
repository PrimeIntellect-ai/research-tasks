You are an incident responder investigating a recent breach on our internal network. An attacker exploited a vulnerable file upload handler to exfiltrate data and drop a custom backdoor. 

We have recovered a suspicious stripped executable that the attacker left behind at `/app/backdoor_beacon`. We suspect this binary is used to phone home or establish a bind shell, but we need you to reverse engineer its behavior.

Your objectives are:
1. **Analyze the Binary**: Determine the protocol and port the `/app/backdoor_beacon` binary uses to communicate. It implements a custom authentication challenge.
2. **Crack the Credentials**: During the breach, the attacker dumped an internal shadow file fragment located at `/home/user/compromised_hashes.txt`. You must crack the hash for the user "admin" to find the password, which we believe is used as the authentication token for the backdoor's protocol.
3. **Develop a Honeypot / Mitigation Service**: Write a Python service that mimics the vulnerable file upload handler but safely sanitizes inputs to prevent path traversal. Additionally, this service must listen on TCP port 8080 and enforce a strict Content Security Policy (CSP) via HTTP headers. The Python service must be saved at `/home/user/secure_upload.py` and actively running.
4. **Configure Network Security**: Write a shell script at `/home/user/firewall_setup.sh` that uses `iptables` to block outgoing connections from the backdoor binary's port, while allowing incoming connections to your Python service on port 8080.

The automated verification system will test your Python service on port 8080 by sending HTTP POST requests to `/upload` with malicious payload attempts (e.g., `../../../etc/passwd`) and expect a safe, sanitized handling or rejection (HTTP 400). It will also check for the presence of the `Content-Security-Policy: default-src 'self'` header. Furthermore, it will attempt to authenticate to your mimicked service using the cracked password.

Please ensure the Python service is running and the firewall script has been executed. Create a log file at `/home/user/incident_report.log` containing the cracked admin password on the first line, and the port used by the backdoor on the second line.