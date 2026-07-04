You are acting as a compliance analyst and security engineer. We need to implement a secure, high-performance audit trail pipeline to satisfy our compliance requirements. 

Our application stack currently consists of an Nginx reverse proxy and a Redis cache. Your task is to write a Rust-based Intrusion Detection System (IDS) and log aggregator that analyzes access logs, cross-references threat intelligence from Redis, identifies malicious payloads, and securely archives the findings using encryption.

Here is the setup:
1. Under `/app/start_services.sh`, there is a script that starts our multi-service environment (Nginx on port 8080, Redis on port 6379). Nginx logs its requests to `/home/user/logs/access.log`.
2. Redis contains a Redis SET named `threat_patterns` containing malicious regex patterns (e.g., SQLi, XSS signatures).
3. In `/home/user/keys/audit.key`, there is a 32-byte hex-encoded encryption key.

Your objective:
1. Create a Rust project in `/home/user/ids_analyzer`.
2. Write a Rust program that reads `/home/user/logs/access.log`.
3. Connect to Redis (localhost:6379) and fetch all regex patterns from the `threat_patterns` SET.
4. Scan every line in the access log. If the URL path or query parameters match ANY of the malicious regex patterns from Redis, flag the log entry.
5. Encrypt the flagged log entries using AES-256-GCM. Use the key provided in `/home/user/keys/audit.key`. For the initialization vector (IV/Nonce), use a static 12-byte nonce: `000000000000000000000000` (12 zero bytes) for simplicity in this specific compliance test.
6. Write the encrypted output (raw bytes, concatenated back-to-back, each prefixed by a 2-byte big-endian length header of the encrypted payload length) to `/home/user/secure_audit/audit.enc`.
7. Apply strict file permissions: The directory `/home/user/secure_audit` must be restricted to `0700` and `audit.enc` must be exactly `0600`.

To complete the task:
- Ensure the Nginx and Redis services are running.
- Build your Rust program in release mode (`cargo build --release`).
- Run the traffic generator script provided at `/app/generate_traffic.py` to simulate 20,000 requests. 
- Run your Rust program to process the logs and generate the encrypted file.

A verification script will grade your Rust program based on its F1-score for correctly identifying and encrypting only the malicious log lines without altering the original log text format within the ciphertexts. You must achieve an F1-score of at least 0.95.