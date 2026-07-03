You are a network engineer inspecting intercepted traffic logs from a critical internal API. Recently, there have been reports of unauthorized access attempts and potential rogue servers being spun up to intercept credentials. 

Your job is to parse the captured traffic logs, validate the server identities, and verify the authorization tokens. 

You have been provided with the following files in the `/home/user/inspect/` directory:
1. `traffic_logs.json`: A JSON array where each object represents a logged connection. Each object contains:
   - `session_id`: A unique string identifier for the session.
   - `server_cert`: The PEM-encoded X.509 certificate presented by the server during the TLS handshake.
   - `auth_token`: A JSON Web Token (JWT) sent by the client.
2. `ca/`: A directory containing the trusted certificate chain:
   - `/home/user/inspect/ca/root.pem`: The Root CA certificate.
   - `/home/user/inspect/ca/intermediate.pem`: The Intermediate CA certificate.
3. `jwt_public.pem`: The RSA public key used to verify the JWT signatures.

Your task is to write a script (in the language of your choice) to process `traffic_logs.json` and find all `session_id`s that meet **both** of the following criteria:
1. **Valid Certificate Chain**: The `server_cert` must be valid and successfully verify against the provided root and intermediate CA certificates.
2. **Valid Auth Token**: The `auth_token` must have a valid RS256 signature that can be verified using `jwt_public.pem`. (You do not need to check for token expiration, only the signature).

Write the `session_id` of every connection that passes both checks to a file located at `/home/user/verified_sessions.txt`. 
The file should contain exactly one `session_id` per line, sorted in alphabetical order. 

You may use standard command-line tools (like `openssl`) or install standard libraries (like `PyJWT` if you choose Python) to complete this task.