You are a forensics analyst responding to a compromised host. The attacker has deployed a custom data exfiltration stack and obfuscated the application logs. We need to recover the environment, secure it, and reverse-engineer the attacker's log obfuscator to analyze the stolen data.

Your task has three main phases:

**Phase 1: Environment Restoration and Securing (Multi-Service)**
The attacker's infrastructure is located in `/app/`. It consists of:
1. A Redis instance (port 6379) storing log file integrity hashes.
2. A vulnerable Flask application (port 5000) that the attacker used to process data.
3. An Nginx reverse proxy.

You must run `/app/start_services.sh` to start Redis and Flask. 
Then, configure the Nginx server by editing `/app/nginx.conf` and starting it. You must:
- Generate a self-signed TLS certificate (`/app/cert.pem` and `/app/key.pem`) and configure Nginx to listen on port 8443 with TLS enabled.
- Proxy all requests from Nginx (`https://localhost:8443/`) to the Flask application (`http://localhost:5000/`).
- Enforce a Content Security Policy by adding the exact header: `Content-Security-Policy: default-src 'self';` to the Nginx responses.

**Phase 2: Vulnerability Exploitation & Discovery**
The Flask application running on port 5000 has a Server-Side Template Injection (SSTI) vulnerability on the `/render?tmpl=` endpoint. 
Exploit this vulnerability locally to read the contents of `/app/secret_seed.txt`. The attacker's obfuscator tool uses this secret seed to encrypt the logs.

**Phase 3: Log Obfuscator Replication**
The attacker left behind a stripped compiled binary at `/app/log_obfuscator_oracle` which they used to mangle the log data. Our automated forensics pipeline cannot use this binary directly; it requires a pure Python implementation.

You must write a Python script at `/home/user/log_processor.py`.
This script must behave exactly identically (bit-exact equivalent) to the attacker's `/app/log_obfuscator_oracle`. 
- Both the oracle and your script must accept a continuous hexadecimal string via standard input (`stdin`).
- Both must output the resulting obfuscated data as a hexadecimal string to standard output (`stdout`), with a trailing newline.
- The oracle internally reads `/app/secret_seed.txt`. Your script should also read this file to obtain the key.
- You can probe the `/app/log_obfuscator_oracle` with different inputs to observe its output and reverse-engineer the simple transformation it applies (it uses a combination of XOR with the secret seed and bitwise rotation).

Ensure `/home/user/log_processor.py` is executable and works correctly for any arbitrary hex string input of length 10 to 100 characters. Our automated testing will verify your script against the oracle using random fuzzing.