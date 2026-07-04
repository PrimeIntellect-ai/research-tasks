You are acting as a security auditor for a vulnerable internal application. The system consists of multiple microservices that have been hastily deployed. Recently, it was discovered that sensitive authentication tokens are being leaked via command-line arguments, which are briefly visible in `/proc` to any user on the system, and get captured in process execution logs.

Your objective is to secure the system architecture, harden access, and conduct an audit of historical logs to identify compromised tokens.

The application stack is located in `/app/` and runs as the current user. It comprises:
1. **Nginx** (Reverse Proxy): Listening on `127.0.0.1:8080`, forwarding requests to Flask. Configured via `/app/nginx.conf`.
2. **Flask API** (`/app/api.py`): Listening on `127.0.0.1:5000`. It receives requests, generates a secure token, and spawns a background worker.
3. **Background Worker** (`/app/worker.py`): Currently spawned by the Flask API using `subprocess.Popen(['python', '/app/worker.py', '--token', '<TOKEN>'])`. This is the source of the leak.
4. **Redis**: Listening on `127.0.0.1:6379`. Currently running but underutilized.
5. **OpenSSH Server**: Listening on `127.0.0.1:2222`. Configured via `/app/sshd_config`.

You must perform the following tasks:

**Phase 1: Architecture Remediation (Code & Multi-Service Configuration)**
Modify `/app/api.py` and `/app/worker.py` so that tokens are NO LONGER passed via command-line arguments. Instead, the Flask API must push the token to a Redis list named `auth_tasks`. The worker must be modified to act as a continuous daemon that blocks and pops tokens from the `auth_tasks` Redis list (using `BLPOP` or similar) and processes them.
Ensure the entire flow (Nginx -> Flask -> Redis -> Worker) functions correctly without leaking tokens to the process arguments. 

**Phase 2: SSH Hardening**
The internal SSH server config (`/app/sshd_config`) currently permits password authentication.
Modify `/app/sshd_config` to strictly enforce Key-Based Authentication only (disable passwords). 
Generate a new ED25519 SSH keypair located at `/home/user/.ssh/admin_key` and configure the SSH server to accept this key for the current user.

**Phase 3: Log Parsing and Token Auditing**
A historical process execution log is available at `/app/historical_syslogs.txt`. It contains thousands of lines of `execve` events, some of which contain the leaked tokens.
A token is a base64-encoded JSON Web Token (JWT) or a custom hexadecimal string prefixed with `SEC-`.
Extract all potential tokens from the log file.
You are provided with a validation library at `/app/token_validator.py` containing a function `is_valid_token(token_string)`. Use this to filter out fake/corrupted tokens.
Save all *valid, compromised tokens* to `/app/compromised_tokens.txt`, with one token per line.

An automated verifier will evaluate your success based on the functional correctness of the multi-service flow and a strict numerical metric evaluating your token extraction accuracy.