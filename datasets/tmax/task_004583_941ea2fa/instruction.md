We are upgrading our internal credential rotation infrastructure. The legacy token validation logic is currently housed in a compiled, stripped ELF binary, but we want to natively integrate it into a new secure daemon written in C. 

Your objective is to write and run a C server that securely processes rotation requests over mutual TLS (mTLS), re-implementing the legacy token validation logic internally.

**Requirements:**
1. **Daemon Endpoint:** Write a C program (e.g., `server.c`) that listens on TCP `127.0.0.1:8443`.
2. **mTLS Configuration:** 
   - Use OpenSSL (libssl) to implement the TLS server.
   - The server certificate and key are provided at `/app/certs/server.crt` and `/app/certs/server.key`.
   - The server must require and verify client certificates against the CA certificate at `/app/certs/ca.crt`.
   - **Authorization:** Only allow connections where the client certificate's Subject Common Name (CN) is exactly `Rotation-Admin`. If the CN does not match, either reject the TLS handshake or close the connection immediately.
3. **Token Validation Reverse Engineering:** 
   - A legacy, stripped binary is located at `/app/token_validator`. It takes a single 16-character hex string as a command-line argument and exits with `0` if the token is valid, and `1` if invalid.
   - You must reverse-engineer this binary to understand the mathematical/cryptographic validation rules it applies to the hex string.
   - **Crucial:** Re-implement this validation logic natively in your C server. You must NOT use `system()`, `popen()`, `exec()`, or any method of calling the external binary from your server.
4. **Protocol:**
   - Once a secure connection is established, the client will send a request ending with a newline (`\n`).
   - Format: `ROTATE <service_id> <token>\n` (e.g., `ROTATE db-prod AA11223344556677\n`).
   - If the token is valid according to your reimplemented logic:
     - Generate a new random 12-character alphanumeric password.
     - Append the new credential to `/home/user/creds.log` in the format `<service_id>:<new_password>\n`.
     - Ensure `/home/user/creds.log` has strict `0600` file permissions (only owner read/write). Create it with these permissions if it doesn't exist.
     - Respond to the client with `OK <new_password>\n`.
   - If the token is structurally invalid or fails the mathematical logic:
     - Respond to the client with `ERR INVALID_TOKEN\n`.
   - Close the connection after one request.
5. **Execution:** Keep the server running in the background so the automated verification system can interact with it. Compile it with `-lssl -lcrypto`.

Investigate the binary, write your secure C daemon, compile it, and leave it running.