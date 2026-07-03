You are a security auditor reviewing a proprietary legacy logging and policy enforcement daemon. During your audit of the permissions and logging systems, you discovered a stripped compiled binary located at `/app/log_auditor`. The original source code for this binary has been lost, but it is critical to the company's compliance infrastructure.

The binary is designed to process dashboard access logs from standard input, enforce Content Security Policy (CSP) rules, decrypt the log payload using a custom proprietary stream cipher, redact sensitive personal data, and re-encrypt the payload before writing to standard output. 

Your task is to reverse-engineer `/app/log_auditor` and write a perfectly equivalent Python script located at `/home/user/emulator.py`. Your Python script must produce the exact same standard output as the binary for any valid standard input.

Here is what we know about the binary's behavior:
1. It reads exactly one line of text from standard input.
2. The expected input format is strictly: `CSP: <csp_string> | PAYLOAD: <hex_encoded_payload>`
3. **CSP Enforcement:** The binary parses the `<csp_string>`. If the string does not contain a specific secure directive, it modifies the CSP string to include it.
4. **Cryptanalysis & Decryption:** The `<hex_encoded_payload>` is decrypted into raw ASCII. The encryption uses a weak, custom stream cipher (susceptible to basic linear/differential cryptanalysis or known-plaintext observation).
5. **Sensitive Data Redaction:** Once decrypted, the binary searches for US Social Security Numbers and redacts them.
6. **Re-encryption:** The redacted ASCII payload is encrypted using the *exact same* cipher state sequence and converted back to hex.
7. The binary outputs the modified string in the same format: `CSP: <modified_csp> | PAYLOAD: <modified_hex_payload>`

You must use `objdump`, `strings`, `gdb`, or black-box analysis (sending chosen plaintexts) to deduce the exact CSP rules, the redaction format, and the mathematical formula used by the stream cipher. 

Write your final solution to `/home/user/emulator.py`. It must be executable via `python3 /home/user/emulator.py`. Automated tests will fuzz your script against the original binary using thousands of randomly generated inputs to ensure bit-exact equivalence.