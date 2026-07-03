You are a network security engineer investigating a suspicious network intrusion. You have intercepted several artifacts and need to analyze them to understand the attacker's methods and C2 infrastructure.

Your investigation has multiple stages and requires you to work with multiple languages and tools.

**Phase 1: Audio Analysis and Optimized Cracking**
We intercepted a voicemail left by the attacker at `/app/voicemail.wav`. It contains a spoken clue about the structure of the password they used to encrypt their payload.
You also have an intercepted SHA-256 hash of this password in `/app/target_hash.txt`.
We have provided a reference implementation of a brute-force script at `/app/slow_cracker.py` which takes a prefix and generates hashes. However, it is far too slow to crack the password in a reasonable time.
1. Transcribe the audio file to determine the exact password pattern (it will give you the prefix and the format of the suffix).
2. Write a highly optimized password cracker in a language of your choice (C, Rust, Go, or heavily optimized Python/Perl) to find the password.
3. Save your optimized cracking script or compiled binary runner as an executable file at `/home/user/fast_cracker`. This program must take the target hash as its first command-line argument, print ONLY the cracked password to standard output, and exit.
*Note: Your `fast_cracker` will be evaluated against `slow_cracker.py` using a rigorous performance benchmark. You must achieve a runtime speedup of at least 25x compared to the reference script.*

**Phase 2: Payload Extraction and ELF Analysis**
1. Use the cracked password to decrypt the attacker's archive located at `/app/payload.zip`.
2. Inside, you will find an ELF binary named `uploader_daemon`. This daemon is known to have a file upload handler susceptible to path traversal.
3. Analyze the ELF binary to find the hardcoded HTTP endpoint path used for the vulnerable upload handler (e.g., `/api/v1/upload/...`).

**Phase 3: Certificate Chain Validation**
1. The `uploader_daemon` binary also contains an embedded PEM certificate chain used to communicate with the attacker's C2 server. Extract this certificate chain from the binary.
2. The chain contains 3 certificates (Root, Intermediate, Leaf). Validate the chain to find out which certificate causes the validation to fail (one of them is intentionally invalid/expired).
3. Identify the Common Name (CN) of the invalid certificate.

**Integration: Final Report**
Compile your findings into a strictly formatted JSON file at `/home/user/investigation_report.json` with the following structure:
```json
{
  "cracked_password": "the_plaintext_password",
  "vulnerable_endpoint": "the_extracted_endpoint_string",
  "invalid_cert_cn": "Common Name of the invalid cert"
}
```

Ensure all requested files (`/home/user/fast_cracker` and `/home/user/investigation_report.json`) are present and conform to these exact specifications.