You are a forensics analyst responding to a compromised Linux host. The attacker left behind a suspicious encryption utility, and we believe they are hiding the encryption PIN in a covert local service. 

Your objective is to recover the 5-digit PIN (00000 - 99999) used by the attacker and write it to `/home/user/recovered_pin.txt`.

Here is the intelligence we have gathered:
1. **Service Auditing & Certificate Validation**: The attacker spawned two hidden SSL/TLS services listening on local high ports (between 8000 and 9000). Both services present X.509 certificates, but only one is signed by the attacker's internal Certificate Authority. The CA certificate has been recovered at `/home/user/evidence/ca.crt`. 
   You must scan the local system to find these services, retrieve their certificates, and validate them against `ca.crt`. The certificate that successfully validates against the CA contains a SHA-256 hash in its "Organization" (`O`) field. This hash is the target hash of the PIN.

2. **Reverse Engineering**: The attacker left behind the compiled encryption binary at `/home/user/evidence/locker`. Analyze this compiled Rust binary (using tools like `strings`, `objdump`, or other binary analysis tools) to find the static salt string appended to the PIN before hashing. The binary hashes the PIN using SHA-256 in the format: `SHA256(PIN + SALT)`.

3. **Password Cracking**: Once you have extracted the correct target hash from the validated certificate and the salt from the binary, write a Rust program in `/home/user/cracker/` to brute-force the 5-digit PIN. 

**Requirements:**
- Do not use root/sudo privileges.
- Write the final recovered 5-digit PIN to `/home/user/recovered_pin.txt` (the file should contain only the 5 digits).
- Your password cracking code must be written in Rust. You may use standard Linux command-line tools for auditing, extraction, and validation.