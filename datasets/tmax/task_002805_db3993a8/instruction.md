You are acting as a security auditor investigating a compromised Linux server. We have discovered that a malicious service is intercepting SSH authentication attempts and leaking the credentials via command-line arguments visible in `/proc`. However, the leaked payloads are encoded.

We recovered a screenshot of the attacker's terminal at `/app/server_audit.png`. The image contains the custom encoding parameters used by the malware (an XOR key and an additive constant). 

Your task is to:
1. Extract the encoding parameters from the provided image (`/app/server_audit.png`). You may use tools like `tesseract` to read the text.
2. Write a C program at `/home/user/decoder.c` and compile it to `/home/user/decoder`.
3. The program must take exactly one command-line argument: a hex-encoded uppercase string representing the intercepted payload (e.g., `1A2B3C`).
4. The program must decode the hex string back into bytes, reverse the attacker's encoding (first subtract the additive constant, then XOR with the key), and print the resulting decoded ASCII plaintext to standard output (with no trailing newline). 

The automated test will heavily fuzz your `/home/user/decoder` binary against the attacker's original decoding tool with thousands of random hex-encoded strings to ensure exact behavioral equivalence. Do not implement any extra output formatting.