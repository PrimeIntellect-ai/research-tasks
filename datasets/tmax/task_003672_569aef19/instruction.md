You are a compliance analyst tasked with deploying a secure token-generation and audit-trail system for an internal legacy service. 

Your workflow consists of four main stages:

**Stage 1: Package Auditing and Repair**
We are using a vendored version of the `PyJWT` library located at `/app/PyJWT-2.8.0`. During a recent security audit, an incident response team discovered that the HMAC signature verification logic within this library was tampered with, causing all valid token validations to fail.
1. Inspect the source code of the vendored package.
2. Locate the tampered verification logic for HMAC algorithms and restore it to its correct, secure state (using constant-time comparison).
3. Install the fixed package in your local environment (`pip install -e /app/PyJWT-2.8.0`).

**Stage 2: Reverse Engineering**
You have been provided a compiled Python bytecode file at `/app/generate_key.pyc`. This legacy script contains the hardcoded master secret key previously used by the organization.
1. Reverse engineer or disassemble `/app/generate_key.pyc` to extract the master secret key string. 
2. You will use this key for all JWT signing and validation in Stage 3.

**Stage 3: Token Service (HTTP)**
Write and run a Python HTTP service (e.g., using Flask, FastAPI, or http.server) that listens on `127.0.0.1:8080`. It must implement the following endpoints:
*   `POST /token`: Accepts a JSON payload `{"user": "<username>"}`. Returns a JSON payload `{"token": "<jwt_token>"}` where the token is signed using the `HS256` algorithm and the master secret key extracted in Stage 2. The payload of the JWT must contain the `user` claim.
*   `POST /validate`: Accepts a JSON payload `{"token": "<jwt_token>"}`. If the token is valid, return HTTP 200 with JSON `{"valid": true, "user": "<username>"}`. If the token is invalid or the signature does not match, return HTTP 401.

**Stage 4: Audit Trail Service (TCP)**
Write and run a raw Python TCP service that listens on `127.0.0.1:8081`. 
*   It must accept incoming text strings (each terminated by a newline `\n`).
*   For each received message (excluding the newline character), calculate its SHA-256 cryptographic hash.
*   Append the result to an audit log file located at `/home/user/audit.log` in the exact format: `[<sha256_hex_digest>] <original_message>` (followed by a newline).

**Execution**
Ensure both services (port 8080 and 8081) are running in the background before you finish your task. Do not use any external APIs or require internet access.