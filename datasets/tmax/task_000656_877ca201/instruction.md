You are a forensics analyst responding to a breach on a compromised host. An attacker bypassed authentication on our internal Rust-based microservices by exploiting a vulnerable JSON Web Token (JWT) implementation and exploiting poor network policies. 

You have two objectives:
1. Build a forensic detector to classify recovered JWT payloads.
2. Patch and reconfigure the compromised application stack.

**Objective 1: Forensic JWT Detector (Adversarial Corpus)**
In `/home/user/detector/`, initialize a new Rust binary project (`cargo new .`). Write a CLI tool that takes a single file path as a command-line argument. The file will contain a single raw JWT string.
Your tool must read the JWT, analyze its header and payload, and print exactly `CLEAN` or `EVIL` to standard output. 

A JWT is `EVIL` if ANY of the following are true:
- The `alg` in the header is `none` (case-insensitive, e.g., `None`, `NONE`, `none`).
- The JWT signature is invalid or missing (the valid signing key is `secret_key_123` using HMAC-SHA256).
- The `user_id` claim in the payload contains common SQL injection signatures (specifically, any string containing `' OR`, `UNION SELECT`, or `; DROP` - case-insensitive).

If the JWT is perfectly valid, signed with `secret_key_123`, uses `HS256`, and contains no injection patterns, it is `CLEAN`.
Compile your tool so the binary is available at `/home/user/detector/target/debug/detector`.

**Objective 2: Application Stack Remediation (Multi-Service Compose)**
The compromised application lives in `/home/user/app/`. It consists of:
- Nginx (reverse proxy, port 8000)
- Rust API Backend (port 8080)
- Redis (port 6379)

Currently, the Rust backend binds to `0.0.0.0:8080`, allowing attackers to bypass Nginx entirely. Furthermore, its internal authentication logic accepts `alg=none` tokens.

You must:
1. Modify `/home/user/app/backend/src/main.rs` to bind the API strictly to `127.0.0.1:8080` so it can only be accessed via Nginx.
2. Modify `/home/user/app/backend/src/auth.rs` to fix the JWT validation logic. It must strictly require the `HS256` algorithm, validate the signature using the key `secret_key_123`, and reject any `alg=none` tokens.
3. Start the services by running `/home/user/app/start.sh`.

Ensure that after your fixes, making a request to `http://localhost:8000/api/secure` with a valid JWT succeeds, but requests with malicious JWTs are rejected. Direct external access to port 8080 must be impossible.