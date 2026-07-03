You are an incident responder investigating a recent breach on a web server. The attacker managed to plant a rogue TLS certificate, forge authentication tokens, and execute a path traversal attack. 

You have been provided with an evidence directory at `/home/user/evidence/` containing:
1. `rogue.crt`: A suspicious TLS certificate left on the server.
2. `access.log`: The web server access logs.
3. `wordlist.txt`: A dictionary of weak passwords recovered from the attacker's staging server.

Your task is to analyze the evidence and generate a final incident report. Complete the following objectives:

1. **Certificate Analysis**: Analyze `/home/user/evidence/rogue.crt` and determine its SHA-256 fingerprint.
2. **Vulnerability Analysis**: Scan `/home/user/evidence/access.log` to identify the IP address of the attacker who successfully executed a path traversal attack (look for typical `../` patterns in the requested URL resulting in a 200 HTTP status code).
3. **Token Extraction**: Identify the JWT (JSON Web Token) used by the attacker. The token is located in the `Authorization` header field recorded in the log line of the successful path traversal attack.
4. **Token Brute-Force**: The attacker forged this JWT using a weak HMAC-SHA256 (HS256) secret key. Brute-force the secret key of the extracted JWT using the provided `/home/user/evidence/wordlist.txt`. You may write a script in any language you choose to accomplish this.

Once you have gathered all the information, create a JSON report at `/home/user/incident_report.json` with the exact following structure:

```json
{
  "cert_fingerprint_sha256": "XX:XX:XX:XX:XX:XX:...",
  "attacker_ip": "X.X.X.X",
  "jwt_token": "ey...",
  "jwt_secret_key": "cracked_secret_here"
}
```

Ensure all keys are strictly lowercase and the JSON is valid. The certificate fingerprint should be in uppercase hex separated by colons (standard OpenSSL format).