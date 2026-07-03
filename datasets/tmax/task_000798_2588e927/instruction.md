You are acting as a security auditor investigating a web server that was recently compromised via an open redirect vulnerability in its login flow. You have been provided with a secured evidence package.

Your investigation consists of four phases:

**Phase 1: Evidence Decryption**
There is an encrypted zip file at `/app/evidence.zip`. 
We recovered an audio recording from the compromised server's administrator, located at `/app/audit_interview.wav`. Transcribe this audio file to find the prefix of the password. The administrator states the password prefix in the recording, and mentions that it is followed by a 3-digit PIN.
You must brute-force the remaining 3 digits to extract the contents of `/app/evidence.zip` into `/home/user/evidence/`.

**Phase 2: Log Parsing and Correlation**
Inside the extracted evidence, you will find an `access.log` file. 
Analyze this log to find all IP addresses that successfully exploited the open redirect vulnerability on the `/login?next=` endpoint (i.e., they successfully redirected to a domain containing `evil.com`).
Write the unique IP addresses, one per line, sorted in ascending order, to `/home/user/evil_ips.txt`.

**Phase 3: Oracle Reverse Engineering**
Also inside the evidence folder is a compiled binary named `oracle_redirect`. This binary is the patched, secure version of the redirect handler written by the original developers.
Your task is to reverse-engineer its behavior. It takes a single command-line argument (the target URL or path) and prints the sanitized, safe redirect URL to standard output. 
Experiment with the binary using various inputs (absolute URLs, relative paths, query parameters, protocol relative URLs like `//`, etc.) to understand its validation and sanitization logic.

**Phase 4: Secure Implementation**
Write a Python script at `/home/user/safe_redirect.py` that implements the exact same logic as `oracle_redirect`.
Your script must accept exactly one command-line argument and print the sanitized URL. 
An automated verifier will fuzz your Python script against the `oracle_redirect` binary using thousands of random payloads, URLs, and edge cases. Your script's output must be **bit-exact equivalent** to the oracle's output for all inputs.

Constraints:
- Use standard Python libraries.
- The entry point for the verifier will be `python3 /home/user/safe_redirect.py <input>`.