You are a forensics analyst investigating a compromised Linux host. The attacker left behind a custom HTTP backdoor written in C++ and a packet capture of the malicious traffic exported as an HTTP log. 

Your objective is to audit the backdoor's source code, identify the cryptographic weakness used to conceal the attacker's commands, and recover the actual command sent to the server.

You have the following artifacts to investigate:
1. `/home/user/backdoor.cpp`: The source code of the attacker's C++ HTTP backdoor.
2. `/home/user/traffic.log`: A raw HTTP dump of traffic hitting the backdoor.

Instructions:
1. Inspect `/home/user/traffic.log` to find the HTTP request sent by the attacker. The backdoor processes commands via a specific custom cookie named `X-CMD`. The value is hex-encoded.
2. Analyze `/home/user/backdoor.cpp` to understand how the `X-CMD` cookie is processed and decrypted. Identify the primary Common Weakness Enumeration (CWE) identifier associated with the flawed cryptographic implementation. 
3. Perform a known-plaintext attack to recover the encryption key. You know from threat intelligence that every valid command executed by this backdoor strictly begins with the ASCII string `CMD_`.
4. Write a C++ program at `/home/user/decrypt.cpp` that implements the cryptanalysis, derives the key, and decrypts the full payload found in the `X-CMD` cookie. Compile and run it.
5. Save the final decrypted command (as ASCII text) into `/home/user/recovered_command.txt`.
6. Save the exact CWE ID (e.g., `CWE-123`) representing the cryptographic vulnerability in the backdoor to `/home/user/cwe.txt`.