You are an incident responder investigating a compromised Linux server. The attacker left behind a few artifacts in `/home/user/investigation/`:
1. `malware.bin`: A compiled ELF executable (Go binary) used by the attacker.
2. `exfil_data.enc`: An encrypted log file containing records of exfiltrated data.
3. `server.go`: A backup of the vulnerable internal web service that the attacker exploited to gain initial access.

Your task is to analyze these artifacts, uncover the extent of the breach, and patch the vulnerability. Complete the following objectives:

**Phase 1: Binary Analysis & Decryption**
1. The attacker hardcoded a 32-byte AES key in `malware.bin`. The key is known to start with the string `"AES256Key"`. Extract this key.
2. The file `exfil_data.enc` was encrypted using AES-256-GCM. The first 12 bytes of the file constitute the GCM nonce (standard size), and the remainder of the file is the ciphertext (with the GCM tag appended automatically by Go's standard `crypto/cipher` implementation). 
3. Write a Go program (you can save it anywhere in `/home/user/investigation/`) that uses the extracted key to decrypt `exfil_data.enc`.
4. Save the plain-text decrypted output exactly to `/home/user/investigation/decrypted.log`.

**Phase 2: Log Parsing**
1. Parse `/home/user/investigation/decrypted.log`. Each line follows the format:
   `[TIMESTAMP] | ACTION | IP: [IP_ADDRESS] | DETAILS`
2. Extract all unique IP addresses where the ACTION is exactly `exfil_success`.
3. Output the sorted, unique IP addresses to `/home/user/investigation/attacker_ips.txt` (one IP per line).

**Phase 3: Code Auditing & Patching**
1. Audit `/home/user/investigation/server.go`. It is a simple Go HTTP server. Identify the Path Traversal vulnerability (CWE-22) in the `/download` handler. The handler is supposed to only serve files from the `/var/www/uploads/` directory based on the `file` query parameter.
2. Patch `server.go` so that it safely sanitizes the input and rejects any request that attempts to read files outside of `/var/www/uploads/`. If a path traversal attempt is detected or the file is invalid, it must return an `http.StatusBadRequest` (400) or `http.StatusForbidden` (403) or `http.StatusNotFound` (404), but it MUST NOT crash or serve the file.
3. Compile your patched Go code into an executable named `/home/user/investigation/server_patched`.

Ensure all requested final files (`decrypted.log`, `attacker_ips.txt`, `server_patched`) are exactly at the specified paths. You may use standard Linux CLI tools and the Go compiler.