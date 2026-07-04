You are an expert security auditor. We have a legacy microservice architecture that is currently failing its integration tests due to misconfigured routing, and we suspect the internal authentication binary is vulnerable to malicious JWTs and payload injection.

You have two main objectives:

**Phase 1: Multi-Service Reconfiguration**
The application lives in `/app/`. It consists of three services managed by `/app/start.sh`:
1. `nginx` (listening on port 8080, acting as the API gateway).
2. `auth_svc` (a pre-compiled internal Rust authentication binary running on port 8081).
3. `audit_backend` (a Flask service running on port 8082).

Currently, `nginx` is completely misconfigured. You must edit `/app/nginx.conf` so that:
- Any request to `/api/auth` is routed to `auth_svc` at `127.0.0.1:8081`.
- Any request to `/api/audit` is routed to `audit_backend` at `127.0.0.1:8082`.
- The `X-Forwarded-For` header is correctly passed to the backend services.
Ensure you restart or reload the services using `/app/start.sh` so the end-to-end routing works correctly. You can test routing by sending a simple GET to `http://127.0.0.1:8080/api/audit/health`.

**Phase 2: Vulnerability Analysis & Rust Detector Implementation**
We have captured a corpus of JWT token authorization logs, but we do not have the source code for the `auth_svc` binary. The binary validates tokens and logs permissions. 

Your task is to build a standalone Rust CLI application in `/home/user/detector` that acts as a security filter. It must parse a directory of JSON log files (each containing an HTTP request dump with an `Authorization: Bearer <token>` header) and classify them as either `CLEAN` or `EVIL`. 

To do this accurately, you must:
1. **Reverse Engineer:** Analyze the `/app/bin/auth_svc` binary to extract the hardcoded HMAC secret key used for JWT signature verification.
2. **Security Parsing:** Write the Rust tool to validate the tokens using the extracted secret.
3. **Vulnerability Detection:** Flag a log as `EVIL` if ANY of the following are true:
   - The token uses the `alg: "none"` vulnerability.
   - The token signature is invalid (does not match the extracted HMAC key).
   - The decoded JWT payload contains obvious SQL injection (e.g., `' OR 1=1`, `--`) or XSS payloads (e.g., `<script>`, `javascript:`) in the `username` or `role` claims.

**Detector Usage Specifications:**
- Project path: `/home/user/detector` (use `cargo init` to create it).
- Command-line invocation: `cargo run --release -- <path_to_corpus_directory>`
- Output format: For every file in the directory, print exactly one line to `stdout` in the format: `<filename>: <CLEAN|EVIL>`. Example:
  `log_001.json: CLEAN`
  `log_002.json: EVIL`

You must ensure your Rust code compiles successfully. An automated testing suite will run your compiled detector against two hidden directories (one full of clean logs, one full of malicious logs) and expects 100% accuracy.