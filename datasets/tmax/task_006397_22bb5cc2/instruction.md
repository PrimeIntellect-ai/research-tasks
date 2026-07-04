You are a security engineer responsible for rotating credentials and securing a web service after a suspected leak of the old JWT signing key. You need to perform certificate rotation, generate a new administrative token, and analyze recent authentication logs to block attackers who exploited the leaked key.

Perform the following tasks in the `/home/user` directory:

1. **Certificate Management & Chain Validation:**
   The service needs new TLS certificates. 
   - Generate a new self-signed Root CA (RSA 2048-bit). Save the private key to `/home/user/certs/ca.key` and the certificate to `/home/user/certs/ca.crt` (valid for 365 days).
   - Generate a leaf private key `/home/user/certs/server.key` (RSA 2048-bit) and a CSR.
   - Use the Root CA to sign the leaf certificate for the Common Name (CN) `secure.localnet`. Save this to `/home/user/certs/server.crt` (valid for 365 days).
   - *Requirement:* Running `openssl verify -CAfile /home/user/certs/ca.crt /home/user/certs/server.crt` must return `OK`.

2. **Token Generation:**
   The old JWT secret was compromised. The new secret is `NewSecureRotatedSecret_99!`.
   - Write a Python script to generate a new JWT using the `PyJWT` library (algorithm: `HS256`).
   - The token payload must contain exactly the following claims:
     `{"sub": "admin", "role": "superuser", "rotated": true}`
   - Save ONLY the raw JWT string to the file `/home/user/new_token.txt`.

3. **Intrusion Detection & Firewall Policy Prep:**
   You have been provided an authentication log at `/home/user/logs/auth.log`.
   - The log contains lines in the format: `[TIMESTAMP] IP: <ip_address> Token: <jwt_string>`
   - Write a Python script to parse this log file. For each line, extract the token and decode its payload (do not verify the signature, as they were signed with the old leaked key).
   - Look for tokens where the payload contains the claim `"malicious": true`.
   - Extract the IP addresses associated with these malicious tokens.
   - Write the unique malicious IP addresses to `/home/user/blocked_ips.txt`, with one IP address per line, sorted in ascending numerical order (e.g., 10.0.0.1 before 10.0.0.2).

Ensure all files are placed in their exact specified locations. You may install the `PyJWT` library via pip if it is not already installed.