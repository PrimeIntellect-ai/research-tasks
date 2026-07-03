You are a compliance analyst tasked with generating an audit trail of unauthorized access attempts from a batch of encrypted security logs.

You have been provided with the following files:
- `/home/user/logs.enc`: An AES-256-CBC encrypted file containing newline-separated JSON objects.
- `/home/user/ca.pem`: The trusted Certificate Authority (CA) root certificate.

The password to decrypt `logs.enc` is `audit_pass_2024`. It was encrypted using OpenSSL with the `-pbkdf2` flag.

Once decrypted, each line of the log file is a JSON object representing a TLS connection attempt, containing the following fields:
- `session_id` (string)
- `client_ip` (string)
- `client_cert_pem` (string): The client's certificate in PEM format.

Your task:
1. Decrypt `/home/user/logs.enc`.
2. Write a Rust program at `/home/user/audit/src/main.rs` (create the Cargo project at `/home/user/audit`) that parses the decrypted logs.
3. For each log entry, your Rust program must extract the `client_cert_pem` and validate it against the trusted `/home/user/ca.pem`. (You may shell out to `openssl verify` from within your Rust code).
4. If a client certificate is INVALID (fails validation), your program should correlate this event by appending a line to `/home/user/invalid_sessions.log` in the exact following format:
   `SESSION_ID: <session_id> | IP: <client_ip>`
5. Once your Rust program has processed all logs and generated `/home/user/invalid_sessions.log`, encrypt this output file to `/home/user/invalid_sessions.enc` using `aes-256-cbc` with the `-pbkdf2` flag and the same password (`audit_pass_2024`).

Ensure the final encrypted file `/home/user/invalid_sessions.enc` is present and correctly formatted.