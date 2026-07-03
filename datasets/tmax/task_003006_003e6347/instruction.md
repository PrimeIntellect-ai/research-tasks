You are a network security engineer investigating a series of anomalous file transfers on an internal network. You have intercepted an audio transmission containing the attacker's authorization passphrase, located at `/app/intercept_77.wav`. 

Your objective is to build a secure network inspection honeypot in **Rust** that mimics the attacker's command-and-control (C2) receiving server to capture and analyze their payloads.

Follow these steps to complete the task:

1. **Audio Analysis:** Determine the spoken passphrase within `/app/intercept_77.wav`. Compute the SHA-256 hash of this passphrase (all lowercase, no punctuation, single spaces between words, no trailing newline).

2. **TLS Setup:** Generate a self-signed TLS certificate (`cert.pem`) and private key (`key.pem`) in `/home/user/`.

3. **Service Implementation (Rust):**
   Create a Rust HTTPS web server project at `/home/user/c2_honeypot`. You may use standard web frameworks like `axum`, `actix-web`, or `warp`.
   The server must:
   - Listen on exactly `127.0.0.1:8443` using the TLS certificate generated above.
   - Expose a `POST /analyze` endpoint.
   
4. **Security Inspection Rules:**
   For incoming requests to `POST /analyze`:
   - **Authentication:** Inspect the HTTP headers for a `Cookie` named `session`. The value of this cookie must exactly match the SHA-256 hash of the passphrase you extracted from the audio. If the cookie is missing or invalid, return a `401 Unauthorized` HTTP status code.
   - **Binary Format Analysis:** The request body will contain raw bytes. You must parse the first 4 bytes of the body to verify if it is a valid ELF binary (Magic bytes: `7F 45 4C 46`). If it is NOT a valid ELF, return a `400 Bad Request` HTTP status code.
   - **Cryptographic Hashing:** If the authentication succeeds and the payload is a valid ELF, compute the SHA-256 hash of the entire raw request body.
   - **Response:** Return a `200 OK` status. The response body must be plain text containing exactly the hex-encoded SHA-256 hash of the payload.

5. **Execution:** Ensure the Rust server is compiled in release mode and running in the background listening on `127.0.0.1:8443` before concluding your turn. Output a log file at `/home/user/server.log` confirming the server has started.