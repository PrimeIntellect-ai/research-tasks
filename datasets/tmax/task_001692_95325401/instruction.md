You are a forensics analyst investigating a compromised Linux host. The attacker deployed a custom backdoor across a multi-service web architecture and left traces of their activity. Your objective is to restore the forensic staging environment, crack the attacker's authentication token, and build a Rust-based detection tool to classify malicious payloads.

**Stage 1: Reconstruct the Staging Environment**
The captured application stack is located in `/app/staging/`. It consists of Nginx, Redis, and a vulnerable API backend. The configuration was corrupted during the forensic capture.
1. Fix the Nginx configuration at `/app/staging/nginx/nginx.conf`. It must listen on port 8080 and proxy all requests starting with `/api/` to the backend service running on `127.0.0.1:8081`.
2. Start the Redis server using the config `/app/staging/redis/redis.conf` (runs on default port 6379).
3. Start the backend service located at `/app/staging/backend/api_server`.
Ensure all three services are running concurrently and successfully communicating (Nginx -> API -> Redis). 

**Stage 2: Forensics & Cryptanalysis**
The attacker left a suspicious network capture log in `/app/evidence/backdoor_requests.log`. 
The backdoor uses a custom authentication header: `X-Backdoor-Auth: <MD5_HASH>`. 
Through reverse engineering, we know the hash is generated as: `MD5(PIN + HTTP_METHOD + URI)`. The PIN is a 4-digit numeric code (e.g., `0000` to `9999`).
Analyze the first request in `backdoor_requests.log`, perform a brute-force search to find the attacker's 4-digit PIN, and save just the 4-digit PIN to `/home/user/cracked_pin.txt`.

**Stage 3: Build the Payload Detector**
You must write a Rust-based detection tool to analyze network payloads and identify the attacker's traffic.
1. Initialize a new Rust executable project at `/home/user/detector`.
2. The program must accept a single command-line argument: a path to a directory containing payload files (`.txt`).
3. Your detector must analyze every `.txt` file in the directory and classify it as malicious if it contains ANY of the following:
   - Typical SQL Injection patterns (e.g., `UNION SELECT`, `' OR '1'='1`)
   - Cross-Site Scripting (XSS) patterns (e.g., `<script>`, `javascript:`, `onerror=`)
   - A valid backdoor request containing the `X-Backdoor-Auth` header where the hash correctly matches the `MD5(PIN + HTTP_METHOD + URI)` using the PIN you cracked in Stage 2. (Assume the first line of the file is always `METHOD URI HTTP/1.1`).
4. For each file, the program must print to `stdout` EXACTLY one line in the format:
   `[CLEAN] filename.txt` OR `[MALICIOUS] filename.txt`.

You have a sample set of logs in `/app/evidence/samples/` to test your detector. When you are finished, leave the detector source code in `/home/user/detector` and ensure it can be compiled via `cargo build --release`. 
An automated verification script will compile your detector and run it against a hidden adversarial corpus.