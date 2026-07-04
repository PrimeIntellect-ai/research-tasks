You are an incident responder investigating a breach in a company's internal data processing pipeline. Attackers successfully submitted malicious payloads by exploiting a vulnerability in the pipeline's authentication token parser (similar to a JWT `alg=none` bypass). 

Your objective is to secure the pipeline, fix the authentication code, enforce data redaction, and correctly wire the microservices back together.

The pipeline lives in `/home/user/app/` and consists of three components:
1. **Nginx** (Reverse Proxy): Should listen on port 8080 and forward traffic to the Flask application.
2. **Flask API** (Log Receiver): Listens on port 5000, validates incoming authentication tokens, and pushes valid log payloads to a Redis queue.
3. **Redis**: Message broker listening on port 6379.
4. **Data Redactor Worker**: A Python daemon that pulls messages from the Redis queue `log_queue`, redacts sensitive data, and writes the output to `/home/user/app/secure_logs.txt`.

### Task 1: Fix the Authentication Module
The token parsing logic in `/home/user/app/auth.py` is vulnerable. It currently accepts tokens where the algorithm is specified as `"none"` or if the signature is missing.
You must rewrite the `verify_token(token_str)` function (and the script's command-line execution block) to perfectly match a secure reference implementation. 
The reference oracle is located at `/opt/oracle/token_verifier`. 
Your script `/home/user/app/auth.py` must take a single token string as a command-line argument and print exactly one of the following strings to standard output:
- `VALID`
- `INVALID_SIGNATURE`
- `INVALID_FORMAT`
- `UNSUPPORTED_ALG`

The token format is `base64(header).base64(payload).base64(signature)`. The shared secret for HMAC-SHA256 is `secret_key_123`. The only supported algorithm is `HS256`. 
Your implementation must be BIT-EXACT equivalent to the oracle. An automated fuzzer will run thousands of malformed, randomized, and valid tokens against both your script and the oracle to ensure identical outputs and error handling.

### Task 2: Implement Sensitive Data Redaction
The log payloads often contain Social Security Numbers (SSNs) in the format `XXX-XX-XXXX`. 
Modify `/home/user/app/worker.py` so that before a log message is written to `/home/user/app/secure_logs.txt`, any SSN is redacted to `***-**-XXXX` (only the last four digits remain visible). 

### Task 3: Compose and Reconfigure the Services
The configuration files were scrambled by the attacker. You must fix them so the services can communicate:
- Fix `/home/user/app/nginx.conf` so it listens on `127.0.0.1:8080` and proxies requests to `http://127.0.0.1:5000`.
- Fix `/home/user/app/config.py` so the Flask app connects to Redis on `127.0.0.1:6379`.
- Ensure `/home/user/app/worker.py` correctly connects to the same Redis instance.

Once you have completed the fixes, ensure that a test payload sent to `http://127.0.0.1:8080/submit` with a valid `Authorization: Bearer <token>` header successfully results in a redacted entry in `/home/user/app/secure_logs.txt`.