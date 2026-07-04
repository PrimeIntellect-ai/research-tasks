You are a DevOps engineer tasked with debugging and fixing a log sanitization pipeline. We have a multi-service architecture that processes incoming application logs, sanitizes them of PII (Personally Identifiable Information), and stores them in Redis for analysis.

Currently, the custom Rust-based log sanitizer service is failing. It panics on certain poorly formatted logs (format parsing edge-cases) and fails to properly filter some malicious/PII payloads. 

Your task is to fix the Rust log sanitizer so that it correctly parses all logs, strips out PII (specifically, any JSON field named "ssn" or "credit_card", and any string value matching the regex pattern `\b\d{3}-\d{2}-\d{4}\b`), and successfully forwards the sanitized logs to Redis. 

Here is the setup:
- The services are located in `/home/user/app/`.
- There is a `startup.sh` script in `/home/user/app/` that starts the Redis server on port 6379 and the Rust sanitizer service on port 8080.
- A test suite of log files is located in `/home/user/corpus/`. It contains two directories: `clean/` and `evil/`.
- The Rust project is located in `/home/user/app/sanitizer/`.

Requirements:
1. Debug and fix the Rust code in `/home/user/app/sanitizer/src/main.rs`. Use the provided test corpus and fuzz testing techniques to identify the edge cases causing the JSON parser to panic.
2. Implement assertion-based validation in the Rust code to ensure no PII fields are emitted.
3. Ensure the service integrates correctly with Redis. You may need to adjust the environment variables in `/home/user/app/.env` to configure the correct Redis connection string and ports.
4. The service must pass the adversarial corpus test. We will run an automated script that sends all files from `/home/user/corpus/evil/` and `/home/user/corpus/clean/` to your Rust service via POST requests to `http://localhost:8080/sanitize`. 
5. For the `clean/` corpus, 100% of the logs must be accepted and preserved unmodified in their JSON structure (stored in Redis).
6. For the `evil/` corpus, 100% of the logs must be parsed without crashing, have the specified PII stripped or redacted (replaced with `[REDACTED]`), and then stored in Redis.

When you have fixed the code, restart the services using `/home/user/app/startup.sh`, and write a log file to `/home/user/solution_status.txt` containing the word "READY".