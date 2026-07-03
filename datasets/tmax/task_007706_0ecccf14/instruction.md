You are an incident responder investigating a suspected compromise of an internal update server. Security tools have flagged anomalous behavior from the update endpoint, including invalid certificates, strange HTTP cookies, and potentially tampered update payloads. 

The suspect server is currently isolated and simulated locally at `https://127.0.0.1:8443`.

Your task is to write a Bash script `/home/user/analyze_endpoint.sh` that automates the triage of this endpoint. You must also run your script and produce a final report.

The script must do the following:
1. Accept four arguments in this exact order: 
   `TARGET_HOST` (e.g., 127.0.0.1), `TARGET_PORT` (e.g., 8443), `TRUSTED_ROOT_CA` (path to the trusted root certificate), and `MANIFEST_FILE` (path to a file containing known good SHA-256 hashes).
2. **Certificate Chain Validation**: Connect to the target host and port via TLS, extract the server's certificate chain, and verify it against the provided `TRUSTED_ROOT_CA`. (Do not worry about hostname verification, only verify the cryptographic chain of trust).
3. **HTTP Header and Cookie Inspection**: Make an HTTP GET request to `https://<TARGET_HOST>:<TARGET_PORT>/update.bin`. Inspect the HTTP response headers to extract the value of the `X-Incident-Token` cookie. (Since the cert might be invalid, ensure your HTTP client is configured to allow the connection to capture the response).
4. **File Integrity Verification**: Download the `update.bin` file from the endpoint. Calculate its SHA-256 checksum and check if this exact hash exists anywhere in the provided `MANIFEST_FILE`.
5. Write the findings to `/home/user/investigation_report.txt` in the following strict format:
```
CERT_STATUS: <VALID or INVALID>
X_INCIDENT_TOKEN: <extracted_cookie_value_here>
FILE_INTEGRITY: <OK or COMPROMISED>
```
If the file's hash is found in the manifest, `FILE_INTEGRITY` is `OK`. Otherwise, it is `COMPROMISED`.

**Setup details:**
* The trusted root certificate you must use for verification is located at `/home/user/ca-trust/root.crt`.
* The known-good manifest file is located at `/home/user/manifest.sha256`.
* Run your script once completed to generate `/home/user/investigation_report.txt`.

Ensure your Bash script is executable (`chmod +x /home/user/analyze_endpoint.sh`). Do not leave any background processes hanging manually; the local test server is already running for you.