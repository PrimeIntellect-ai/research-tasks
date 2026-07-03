You are an incident responder investigating a potential data exfiltration event on a compromised Linux machine. You have collected a network traffic snippet and an encrypted payload. We also recovered a partial C source file left behind by the attacker, which appears to be the encryption/decryption tool.

Your objective is to recover the exfiltrated data, redact any sensitive customer information, and identify the attacker's PIN.

Here is what you have in `/home/user/evidence/`:
1. `/home/user/evidence/headers.txt`: The HTTP request headers used during the exfiltration. The attacker uses a custom `SessionID` cookie.
2. `/home/user/evidence/payload.bin`: The encrypted exfiltration payload.
3. `/home/user/evidence/decryptor_template.c`: A partially wiped C source code file that shows the math behind the `SessionID` generation and the encryption algorithm, but the actual PIN is missing.

Your tasks:
1. **HTTP Header Inspection:** Examine `headers.txt` to find the `SessionID` value. 
2. **Password Cracking / C Programming:** The `decryptor_template.c` file reveals that the `SessionID` is generated from a 4-digit PIN (0000-9999). Write or complete a C program to brute-force this 4-digit PIN by reproducing the math until it matches the `SessionID` found in the HTTP headers.
3. **Decryption:** Once you have the PIN, use your C program to decrypt `payload.bin`. The encryption is a simple byte-wise XOR using `(PIN % 256)` as the key. Save the decrypted plaintext to `/home/user/decrypted.txt`.
4. **Sensitive Data Redaction:** The decrypted file contains stolen credit card numbers (contiguous 16-digit numbers). Use any command-line tool to redact these numbers. Replace every 16-digit contiguous number entirely with the exact string `[REDACTED]`. Save the redacted output to `/home/user/clean_report.txt`.
5. **Reporting:** Save the 4-digit PIN you discovered to a file named `/home/user/pin.txt`.

Verification:
- The system will check the contents of `/home/user/clean_report.txt` to ensure the data is decrypted and properly redacted.
- The system will check `/home/user/pin.txt` for the correct 4-digit PIN.