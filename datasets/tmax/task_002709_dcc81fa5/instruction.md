You are acting as a penetration tester analyzing intercepted server communications to identify compromised endpoints in a target network.

You have been provided with intercepted event logs, a list of revoked TLS certificates, and a reference binary file. You must write a C program that acts as a security log parser and correlation engine.

Your task is to write a C program at `/home/user/analyzer.c` that parses the provided logs, correlates the security indicators, and outputs a list of compromised IP addresses.

Here are the details of the environment and your requirements:

1. **Files Provided:**
   - `/home/user/sec_events.log`: A pipe-delimited (`|`) text log file where each line represents a server event. The columns are: `IP_Address|TLS_Cert_Fingerprint|Content_Security_Policy|Downloaded_File_Hash`
   - `/home/user/revoked_certs.txt`: A text file containing a list of revoked TLS certificate SHA-256 fingerprints, one per line.
   - `/home/user/known_good.bin`: A reference binary payload.

2. **Vulnerability Criteria:**
   An endpoint (IP Address) is considered compromised if and only if it meets **ALL** of the following conditions simultaneously:
   - **Certificate Management:** Its `TLS_Cert_Fingerprint` exactly matches one of the fingerprints listed in `/home/user/revoked_certs.txt`.
   - **Content Security Policy:** Its `Content_Security_Policy` header is weak. Specifically, it is missing the exact substring `default-src 'self'`.
   - **Checksum Verification:** Its `Downloaded_File_Hash` (a hex string in the log) does **NOT** match the SHA-256 hash of `/home/user/known_good.bin`. 

3. **Program Requirements:**
   - Your C program must dynamically calculate the SHA-256 hash of `/home/user/known_good.bin` using OpenSSL's `libcrypto` (you can link with `-lcrypto`). Do not hardcode the hash.
   - It must parse the log file and evaluate each line against the 3 criteria.
   - It must output the compromised IP addresses, one per line, to a file located at `/home/user/compromised_ips.txt`.

Compile your C program, run it, and ensure `/home/user/compromised_ips.txt` is generated with the correct IP addresses.