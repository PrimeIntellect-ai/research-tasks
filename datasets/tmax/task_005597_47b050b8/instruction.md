You are an incident responder investigating a compromised Linux server. You have captured a suspicious HTTP request log and isolated a certificate chain used by the malware for its Command and Control (C2) communication.

Your task is to write a C program at `/home/user/incident/investigate.c` that performs the following steps:

1. **Certificate Chain Validation**:
   - Programmatically validate the C2 certificate chain located at `/home/user/incident/c2_chain.pem` against the trusted root certificate at `/home/user/incident/root.pem` using OpenSSL C APIs.
   - If the certificate chain is invalid, print an error and exit with status code 1.

2. **HTTP Cookie Inspection**:
   - Read the HTTP request log from `/home/user/incident/traffic.log`.
   - Parse the file to extract the value of the `session` cookie (it will be a hex-encoded string).

3. **Decryption**:
   - The cookie value is encrypted using AES-128-CBC. 
   - Read the hexadecimal Key and IV from `/home/user/incident/crypto.txt` (Format: `KEY=...` and `IV=...` on separate lines).
   - Convert the hex-encoded cookie back to binary and decrypt it using the Key and IV. 

4. **Sensitive Data Redaction**:
   - The decrypted payload is a JSON string containing sensitive user data, including Social Security Numbers.
   - Find any SSN matching the pattern `XXX-XX-XXXX` (where X is a digit) in the decrypted plaintext and redact it by replacing all digits with asterisks (`***-**-****`).
   - Write the fully redacted, decrypted string to `/home/user/incident/redacted_payload.txt` without any trailing newlines unless they are part of the original plaintext.

Once you have written the code, compile it using `gcc -o /home/user/incident/investigate /home/user/incident/investigate.c -lssl -lcrypto` and run it to produce the required output file.