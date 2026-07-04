You are a forensics analyst assigned to recover evidence from a compromised host and secure its systems. The host contains a custom Rust-based forensics evidence suite that the attacker exploited. 

The suite is located in `/app/` and consists of two services:
1. `evidence_api`: A Rust HTTP service (Rocket/Actix/Axum based, or standard library) that queries the evidence database.
2. `audit_logger`: A Rust TCP service that records all access logs.

Your objectives:
1. **Security Log Parsing & Password Cracking**: The attacker escalated privileges and left a backdoor password hash in the system logs. Parse `/app/logs/system.log` to find the attacker's SHA-256 hash. The hash corresponds to a 4-digit PIN. Crack the hash and write the plaintext 4-digit PIN to `/app/cracked_pin.txt`.
2. **Injection Vulnerability Analysis & Secure Coding**: The attacker compromised the system using an SQL injection vulnerability in the `evidence_api` service. Inspect `/app/evidence_api/src/main.rs`. The `GET /record?id=<id>` endpoint currently concatenates the `id` directly into an SQLite query string. Refactor the code to use parameterized queries (bind parameters) to prevent SQL injection.
3. **Service Reconfiguration & Composition**: Reconfigure and start both services. 
   - Compile both services using `cargo build --release`.
   - Start `audit_logger` so it listens on `127.0.0.1:9000` (TCP).
   - Start `evidence_api` so it listens on `127.0.0.1:8000` (HTTP) and connects to the `audit_logger` on port 9000. Use the cracked PIN as the value for the `ADMIN_TOKEN` environment variable when starting `evidence_api`.
   - Leave both services running in the background.

The automated verification will:
- Check `/app/cracked_pin.txt` for the correct PIN.
- Send valid HTTP requests to `http://127.0.0.1:8000/record?id=1` to ensure normal functionality.
- Send malicious HTTP requests (e.g., `http://127.0.0.1:8000/record?id=1' OR '1'='1`) to verify the SQL injection has been properly patched.

Ensure your compiled services are actively running on the specified ports before you complete the task.