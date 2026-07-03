You are a compliance analyst tasked with generating an audit trail and remediating a legacy data-processing script. The script currently has severe security flaws, including credential leakage, improper certificate validation, and ignorance of insecure HTTP headers. 

Your objective is to fix the script, process the server's data securely, and generate an audit report.

Here are your specific tasks:

1. **Start the Mock Server**:
   A mock legacy HTTPS server is located at `/home/user/server/server.py`. Start it in the background (it listens on `https://127.0.0.1:8443`). 
   *Note: Ensure the server is running before attempting to test your client script.*

2. **Remediate the Command-Line Credential Leak**:
   The client script, located at `/home/user/vulnerable_client.py`, currently accepts a sensitive authentication token via the `--token` command-line argument. This is a severe compliance violation as it exposes the token to all users on the system via `/proc/[pid]/cmdline`.
   * Modify `/home/user/vulnerable_client.py` to remove the `--token` argument.
   * Instead, the script must read the token securely from the `SECRET_TOKEN` environment variable.

3. **Enforce Certificate Chain Validation**:
   The client script currently connects to the server using `requests.get(..., verify=False)`. This allows man-in-the-middle attacks.
   * Modify the script to validate the server's certificate chain.
   * A trusted Root CA certificate is provided at `/home/user/certs/root_ca.pem`. Configure the `requests` call to use this specific Root CA for validation.

4. **Payload Decoding and Cookie Inspection**:
   When the client connects to the server with the correct token (the expected token is `AuditToken2024`), the server returns a JSON response containing a `payload` field and sets a session cookie.
   * The `payload` field is Base64 encoded. Your script must decode this payload into a standard UTF-8 string.
   * The server sets a cookie in the response. You must inspect the `Set-Cookie` header (or the cookie jar). Identify any cookies that are missing the `Secure` AND/OR `HttpOnly` flags.

5. **Generate the Audit Trail**:
   Based on your remediation and the data received from the server, create an audit report at `/home/user/audit_report.json`. The file must be strictly formatted JSON with the following structure:
   ```json
   {
     "token_env_var_used": "<The name of the environment variable you used>",
     "ca_cert_path": "<The absolute path to the Root CA used for validation>",
     "decoded_payload": "<The decoded UTF-8 string from the server's payload>",
     "insecure_cookies": ["<list of cookie names that lack Secure or HttpOnly flags>"]
   }
   ```

Do not use any external dependencies other than standard Python libraries and the `requests` library.