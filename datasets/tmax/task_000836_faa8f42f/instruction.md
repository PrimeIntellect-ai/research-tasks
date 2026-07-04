You are a forensics analyst investigating a compromised Linux web server. The attacker deployed a custom implant. You have been provided with an archive of forensic artifacts in `/home/user/forensics/`.

Your goal is to complete a multi-phase forensic analysis to determine the vulnerability used, the C2 domain, decode the malicious payload using a custom C program, and identify other infected files. 

All your final evidence must be placed in the `/home/user/evidence/` directory, which you must create.

**Phase 1: Code Auditing (CWE Identification)**
The attacker exploited a custom web module to gain initial access. The source code of this module is located at `/home/user/forensics/upload_handler.c`.
1. Review the C source code and identify the primary vulnerability class that leads to memory corruption.
2. Write the standard CWE identifier (in the format `CWE-XXX`, e.g., `CWE-79`) to `/home/user/evidence/cwe.txt`. (Use the most specific, standard CWE for a classic stack-based buffer overflow).

**Phase 2: Certificate Chain Validation**
The attacker left multiple potential C2 certificates in `/home/user/forensics/certs/`. Only one of the `implant_X.pem` certificates is actually cryptographically valid and signed by the provided CA chain (`ca_chain.pem`).
1. Validate the certificates against the CA chain.
2. Extract the Common Name (CN) of the single valid `implant_X.pem` certificate.
3. Write only the Common Name string to `/home/user/evidence/c2_domain.txt`.

**Phase 3: Payload Decoding**
You found an encoded payload at `/home/user/forensics/payload.enc`. Analysis of the attacker's tools indicates the encoding scheme is:
- The raw binary payload was first XOR'd byte-by-byte with the hex key `0x42`.
- The resulting XOR'd bytes were then Base64 encoded.
1. Write a C program at `/home/user/workspace/decoder.c` that reads `/home/user/forensics/payload.enc`, performs the Base64 decoding, applies the XOR decryption, and writes the resulting binary file to `/home/user/evidence/implant.bin`.
2. Compile and run your C program to produce the decoded binary.

**Phase 4: Pattern Matching for Intrusion Detection**
The decoded `/home/user/evidence/implant.bin` contains a unique 12-character plaintext signature that always starts with `SIG_` followed by exactly 8 uppercase hex characters (e.g., `SIG_1A2B3C4D`).
1. Identify this signature inside `implant.bin`.
2. Write a YARA rule named `Implant_Rule` in `/home/user/evidence/implant.yar` that detects this exact signature as an ASCII string.
3. Use your YARA rule to scan the directory `/home/user/forensics/system_files/`.
4. Save the absolute file paths of all matching infected files to `/home/user/evidence/infected.txt` (one path per line).

Ensure all evidence files exactly match the requested filenames and formats.