You are a security engineer tasked with rotating credentials after detecting anomalous access patterns from a specific malicious subnet.

You have been provided with an API access log at `/home/user/api_requests.log`. 

Your task is to write a C program that identifies compromised API keys, hashes them for safe storage in a revocation list, and outputs the result.

Here is the log format:
`[YYYY-MM-DD HH:MM:SS] IP: <ip_address> Method: <method> Path: <path> Auth: Bearer <api_key> Status: <status_code>`

Requirements:
1. Write a C program located at `/home/user/revoke_keys.c`.
2. The program must read `/home/user/api_requests.log`.
3. It must find all log entries where the IP address belongs to the `198.51.100.0/24` subnet (i.e., starts with `198.51.100.`).
4. For each compromised request, extract the `<api_key>` from the `Auth: Bearer` field.
5. Compute the SHA-256 hash of the extracted API key (excluding any whitespace or newlines). You may use the OpenSSL library (`<openssl/sha.h>`).
6. Write the lowercase hex representation of these SHA-256 hashes to `/home/user/revoked_hashes.txt`.
7. The output file `/home/user/revoked_hashes.txt` must contain exactly one hash per line, and the hashes must be sorted alphabetically. Ensure no duplicate hashes are written to the file.
8. Compile your C program to `/home/user/revoke_keys` (e.g., `gcc -o /home/user/revoke_keys /home/user/revoke_keys.c -lssl -lcrypto`) and run it to produce the output file.