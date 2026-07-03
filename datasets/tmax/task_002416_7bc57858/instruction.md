You are a forensics analyst tasked with recovering evidence and reverse-engineering the command-and-control (C2) infrastructure of a compromised host. We have recovered a malicious ELF binary from the system, located at `/home/user/evidence/implant.bin`.

Through initial triage, we suspect this malware uses HTTPS for communication and authenticates using JSON Web Tokens (JWT). The malware author made a critical mistake: the binary statically embeds the C2 server's TLS certificate, the TLS private key, the JWT HMAC signing secret, and a fallback C2 payload. 

Additionally, we recovered a modified version of the `pyjwt` library the threat actor was using to test their C2 locally, located at `/app/vendored/pyjwt-2.8.0`. The actor intentionally introduced a bug in this vendored package to break signature validation as an anti-analysis measure.

Your task consists of the following steps:

1. **Artifact Extraction (ELF Analysis):**
   Analyze `/home/user/evidence/implant.bin` and extract:
   - The embedded TLS certificate (PEM format).
   - The embedded TLS private key (PEM format).
   - The JWT secret key (look for a string prefixed with `JWT_SECRET:`).
   - The fallback C2 payload (look for a string prefixed with `C2_PAYLOAD:`).

2. **Package Repair:**
   Inspect the vendored package at `/app/vendored/pyjwt-2.8.0`. Find the deliberate perturbation that unconditionally fails JWT signature validation, fix the code, and install the package in your environment (e.g., using `pip install -e /app/vendored/pyjwt-2.8.0`).

3. **C2 Emulation:**
   Write a multi-language or Python-based HTTPS server that acts as the recovered C2 server. 
   - The server must listen on exactly `127.0.0.1:8443`.
   - It must use the extracted TLS certificate and private key to secure the connection.
   - It must expose a `GET /beacon` endpoint.
   - The endpoint must read the `Authorization: Bearer <token>` header.
   - It must decode and verify the JWT token using the repaired `pyjwt` library, the extracted JWT secret, and the `HS256` algorithm.
   - If the token is valid, respond with HTTP 200 OK and a JSON payload exactly matching: `{"status": "ok", "payload": "<extracted C2_PAYLOAD>"}`.
   - If the token is invalid or missing, respond with HTTP 401 Unauthorized.

Start your server so it remains running. Our automated verification suite will connect to `127.0.0.1:8443` via HTTPS, provide a valid JWT signed with the extracted secret, and verify that the server validates the token and returns the correct payload.