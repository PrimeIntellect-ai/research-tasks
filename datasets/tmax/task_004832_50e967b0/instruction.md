You are a network security engineer tasked with securing a microservices environment and creating a traffic inspection filter.

Your environment consists of three services:
1. **Nginx** (Frontend proxy)
2. **Go API Backend** (Handles business logic)
3. **Redis** (Data store)

There are two main objectives:

### Objective 1: Fix the Service Composition (End-to-End Flow)
The services are provided in `/app/`. Nginx is supposed to listen on port 8080 and reverse-proxy requests to the Go API running on port 8443 (HTTPS). The Go API connects to Redis on port 6379.
Currently, the Nginx configuration `/app/nginx/nginx.conf` is broken. The Go API enforces mutual TLS (mTLS). You must reconfigure Nginx so that it:
- Proxies requests from `http://127.0.0.1:8080/` to `https://127.0.0.1:8443/`.
- Authenticates itself to the Go API using the client certificate `/app/certs/client.crt` and private key `/app/certs/client.key`.
- Validates the Go API's certificate chain using `/app/certs/ca.crt`.
Once correctly configured, running `curl http://127.0.0.1:8080/ping` should return `{"status":"ok"}`. You can start Nginx using `nginx -c /app/nginx/nginx.conf`. The Go API and Redis are already running.

### Objective 2: Build a Log Sanitizer and Threat Detector
The system logs HTTP traffic in JSONL format. You must write a Go CLI tool at `/app/filter.go` that reads JSONL logs from standard input and writes sanitized JSONL logs to standard output. 

Your filter must implement the following logic:
1. **Payload Decoding & CWE Identification (Drop Malicious Logs):**
   Each log entry has a `request_payload` string field which is URL-encoded. You must decode this payload. If the decoded payload contains Directory Traversal sequences (`../` or `..\`) or SQL Injection signatures (the exact case-insensitive substrings `UNION SELECT` or `1=1`), you must completely DROP the log entry (do not print it).
2. **Sensitive Data Redaction (Sanitize Clean Logs):**
   If the log entry is not malicious, you must redact sensitive information from the `response_body` field. Specifically, replace any sequence matching the pattern `CRED-[A-Z0-9]{4}-[A-Z0-9]{4}` with `CRED-XXXX-XXXX`.
3. Output the preserved (and potentially redacted) log lines as valid JSON lines to standard output.

Your Go program will be tested against two corpora:
- **Clean Corpus**: Contains benign traffic. Your program must preserve 100% of these log lines, properly redacting any `CRED-` patterns.
- **Evil Corpus**: Contains traffic with CWE-22 and CWE-89 payloads. Your program must reject (drop) 100% of these lines.

Ensure your code is efficient and handles invalid JSON gracefully by skipping it. Build your executable or ensure `go run /app/filter.go < input.jsonl > output.jsonl` works flawlessly.