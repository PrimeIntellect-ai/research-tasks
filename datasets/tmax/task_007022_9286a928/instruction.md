You are acting as a penetration tester analyzing a suspected compromise. You have been provided with web server access logs and a custom C++ decoder utility that was recovered from the compromised system. 

Your goal is to extract suspicious payloads from the logs, decode them, and identify which payload matches a known malicious signature.

Here is the setup:
- **Log File:** `/home/user/pentest_data/access.log` contains HTTP requests. Some requests to the `/api/auth` endpoint contain a `payload=` parameter in the query string. These payloads are hex-encoded.
- **Decoder Source:** `/home/user/pentest_data/decoder.cpp`. The attacker used this utility to decode the payloads. It converts a hex string back to bytes and then XORs each byte with the key `0x7F`. However, the recovered C++ source code has a logical bug and does not decode the entire payload correctly.
- **Signatures:** `/home/user/pentest_data/malicious_hashes.txt` contains a list of SHA-256 hashes of known malicious, plaintext payloads.

Your tasks:
1. Fix the bug in `/home/user/pentest_data/decoder.cpp` so it correctly decodes the *entire* hex payload to plaintext and prints it to standard output. Compile it to `/home/user/pentest_data/decoder`.
2. Parse the `/home/user/pentest_data/access.log` to extract the source IP addresses and their corresponding encoded payloads from the `/api/auth` requests.
3. Process each extracted payload using your compiled `decoder`.
4. Calculate the SHA-256 hash of each decoded payload.
5. Compare the hashes against the signatures in `/home/user/pentest_data/malicious_hashes.txt`.
6. Once you find the match, create a final report at `/home/user/report.txt`. 

The `/home/user/report.txt` file must contain exactly two lines in this format:
```
IP: <Matching_IP_Address>
Payload: <Decoded_Plaintext_Payload>
```

Ensure your C++ program cleanly outputs only the decoded string (no extra newlines or debugging text) so you can hash it accurately.