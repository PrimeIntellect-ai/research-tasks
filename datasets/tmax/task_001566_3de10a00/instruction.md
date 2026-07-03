You are a security engineer tasked with rotating the credentials of a legacy critical system after a suspected data breach. 

The system relies on a master key that was encrypted using a proprietary, internally developed encryption tool. We no longer have the source code for this tool, only the compiled binary located at `/home/user/legacy_encrypt`. 

During the incident, attackers exploited an SQL injection vulnerability in our debug API. We captured the traffic logs, which include the verbose debug responses. The logs are stored in `/home/user/logs/api_requests.log`.

Your objective is to safely rotate this master key by performing the following steps:

1. **Log Parsing & Injection Analysis:** 
   Analyze `/home/user/logs/api_requests.log`. Identify the successful SQL injection payload that leaked the encrypted master key and its Initialization Vector (IV). The application logged the exfiltrated data in a JSON response body.

2. **Reverse Engineering:** 
   Disassemble and reverse-engineer the `/home/user/legacy_encrypt` binary. The binary encrypts data using a custom stream cipher. You need to determine the algorithm and constants used to generate the keystream from the initial IV.

3. **Cryptanalysis / Decryption:** 
   Using the leaked IV and encrypted master key (hex-encoded) from the logs, and the algorithm you recovered from the binary, decrypt the ciphertext to recover the original plaintext master key.

4. **Secure Credential Rotation (C Programming):**
   Write a C program at `/home/user/rotate.c` that:
   - Takes the recovered plaintext master key as a command-line argument.
   - Generates a new secure key by computing the SHA-256 hash of the plaintext master key (you may use OpenSSL).
   - Validates that the input key contains no illegal characters to mitigate future injections (only allow alphanumeric characters and `!`, `@`, `#`, `$`). If invalid characters are found, the program should exit with code 1.
   - Outputs a strict JSON object to `/home/user/new_creds.json` in exactly this format:
     `{"status": "rotated", "new_key": "<sha256_hex_lowercase>"}`

5. Compile your C program (ensure you link necessary libraries like `-lcrypto`) and execute it with the recovered plaintext key to generate `/home/user/new_creds.json`.

Ensure your final JSON file exists and is strictly formatted as requested.