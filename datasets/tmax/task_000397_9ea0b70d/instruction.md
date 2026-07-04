You are a forensics analyst responding to a severe breach on a company's internal network. The attacker managed to compromise an administrative console, bypass authentication, and inject malicious scripts.

We have collected several pieces of evidence:
1. A video capture of the attacker's terminal during the breach, located at `/app/incident.mp4`. This video shows the attacker forging JSON Web Tokens (JWTs) and executing Cross-Site Scripting (XSS) payloads.
2. The web server access logs at `/app/access.log`.
3. A directory of captured TLS certificates at `/app/certs/`, which contains a mix of valid and revoked certificates used by the internal services.

Your objectives are to analyze the evidence and recover the final forensic flag:

**Phase 1: Log Correlation and Video Analysis**
1. Review the video `/app/incident.mp4`. You will notice the attacker exploiting a vulnerability where the server accepts JWTs with no signature.
2. Using Bash, write a script `/home/user/analyze.sh` that parses `/app/access.log`. You must identify the IP addresses of the attackers. An IP is considered malicious if it meets **both** of the following conditions:
   - The IP sent a request containing an obvious XSS payload in the URL (e.g., `<script>`, `javascript:`, or `onerror=`).
   - The IP sent a request with an Authorization bearer token that exploits the "none" algorithm vulnerability. (Hint: Look for JWTs where the base64-encoded header corresponds to `{"alg":"none"}` or similar variations).
3. Have your script output the unique sorted list of malicious IP addresses to `/home/user/malicious_ips.txt`, one IP per line. 

**Phase 2: Authentication Bypass and Certificate Validation**
1. The compromised service has a recovery endpoint running locally at `https://localhost:8443/api/evidence`. 
2. The service enforces TLS, but uses a custom Certificate Authority. In `/app/certs/`, you will find `ca.crt`, `intermediate.crt`, and `server.crt`. You must validate the chain to ensure it is intact.
3. Once validated, construct a forged JWT entirely in Bash. The token must have the header `{"alg":"none","typ":"JWT"}` and the payload `{"user":"admin","role":"superuser"}`. Ensure it is correctly Base64URL encoded and formatted as a JWT (Header.Payload.Signature), where the signature is empty.
4. Use `curl` to send a GET request to `https://localhost:8443/api/evidence`, passing the forged JWT in the `Authorization: Bearer <token>` header, and using the correct certificate chain from `/app/certs/` to verify the connection.
5. Save the output of the curl command (which contains the forensic flag) to `/home/user/flag.txt`.

Ensure your log parsing script is efficient, as it will be evaluated against a metric for accuracy (F1-score) based on the IPs you identify.