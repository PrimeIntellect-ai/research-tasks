You are a forensics analyst investigating a compromised host. The server runs a multi-service web application consisting of Nginx, a Python Flask API, and a Redis cache. The attacker managed to exploit a vulnerability via malicious HTTP headers, escalated privileges by breaking out of the application's sandbox, and exfiltrated a highly sensitive document by fragmenting it and hiding it inside the Redis cache before crashing the application.

Your objectives are to restore the services, analyze the attack vector, and recover the fragmented evidence.

1. **Service Restoration**:
   The application environment is located in `/app/services/`. The attacker altered the configuration, causing the end-to-end flow to fail. 
   - Reconfigure the Nginx configuration (`/app/services/nginx.conf`) and the Flask environment variables (`/app/services/.env`) so that Nginx (listening on port 8080) correctly proxies requests to the Flask app (port 5000), and the Flask app can connect to Redis (port 6379).
   - Use the provided `/app/services/start.sh` to launch all three services. Verify that a `GET /health` request to port 8080 returns a 200 OK status.

2. **Privilege Escalation & Sandbox Auditing**:
   The Flask app was supposed to run in a restricted sandbox. Identify the misconfigured SUID binary in `/app/sandbox/bin/` that the attacker used for privilege escalation. Document the name of this binary and the exact command the attacker used to exploit it in a file named `/home/user/audit_report.txt`.

3. **Evidence Recovery (Python Implementation)**:
   The attacker fragmented a sensitive document and stored the pieces in Redis as key-value pairs (keys are formatted as `payload_<hash>`).
   - Analyze the network traffic capture `/app/evidence/traffic.pcap` and Nginx logs `/app/evidence/access.log`. The attacker exfiltrated the correct ordering of the fragments by sending specific HTTP Cookies (containing the `<hash>`) and custom HTTP headers (`X-Exfil-Order`) to the server.
   - Write a Python script at `/home/user/recover.py` that parses the PCAP/logs to extract the mapping between the ordering and the payload hashes.
   - The script must connect to the local Redis instance, retrieve the fragments, reassemble the document in the correct order, and save the final reconstructed text to `/home/user/recovered_evidence.txt`.

Your success will be measured by an automated verifier that computes the string similarity between your `/home/user/recovered_evidence.txt` and the original intact document. You must achieve a similarity score of 0.98 or higher.