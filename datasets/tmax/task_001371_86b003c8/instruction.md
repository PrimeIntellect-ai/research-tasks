You are an incident responder investigating a recent data breach. The attacker exfiltrated a sensitive file, but they encrypted it using a custom lightweight C program before transferring it out. We managed to intercept the encrypted file, the SHA256 checksum of the original file, and the source code of the attacker's malware.

Your goals are to recover the original file, verify its integrity, and redact the sensitive information so the safe file can be shared with management.

Here is the situation:
- **Malware Source:** `/home/user/incident/malware.c` (Contains the encryption algorithm, which uses a Linear Congruential Generator (LCG) for a stream cipher).
- **Encrypted File:** `/home/user/incident/exfil.enc`
- **Original Hash:** `/home/user/incident/checksum.sha256` (Contains the SHA256 hash of the original plaintext file).

**Cryptanalysis & Decryption:**
The malware uses a weak LCG with a 16-bit seed (values from 0 to 65535). The LCG state updates per byte. 
We know the original plaintext file always starts with the known string: `CUSTOMER_DATA_START`
You must write a C program at `/home/user/incident/decrypt.c`, compile it, and use it to recover the original plaintext. Your program should exploit the weak keyspace and known plaintext to find the correct seed and decrypt the file.
Save the successfully decrypted file to `/home/user/incident/exfil_recovered.txt`.

**Integrity Verification:**
Verify that your recovered file's SHA256 hash matches the hash provided in `/home/user/incident/checksum.sha256`. 

**Sensitive Data Redaction:**
The recovered file contains credit card numbers in the format `DDDD-DDDD-DDDD-DDDD` (where `D` is a digit). 
You must redact these numbers by replacing the first 12 digits and their dashes with `XXXX-XXXX-XXXX-`, leaving only the last 4 digits visible. 
For example, `1234-5678-9012-3456` must become `XXXX-XXXX-XXXX-3456`.
Save the redacted file as `/home/user/incident/exfil_redacted.txt`.

Ensure all requested output files (`exfil_recovered.txt` and `exfil_redacted.txt`) exist in `/home/user/incident/` with the exact correct contents.