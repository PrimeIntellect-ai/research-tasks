You are a forensics analyst investigating a compromised Linux web server. The attacker exfiltrated data, left a backdoor, and encrypted a payload containing stolen intellectual property. All evidence has been collected in the `/home/user/evidence` directory.

Your objective is to clean the exfiltrated logs of sensitive data, reverse-engineer the attacker's authentication mechanism, recover the encrypted payload, and verify its integrity.

Perform the following tasks:

1. **Sensitive Data Redaction:**
   The file `/home/user/evidence/capture.log` contains captured raw HTTP requests. Some of these requests contain sensitive cookies. You must create a new file at `/home/user/evidence/redacted_capture.log` that is identical to `capture.log`, EXCEPT that any values for `session_token` and `password` inside the `Cookie:` headers must be replaced with the exact string `[REDACTED]`. 
   *(Example: `Cookie: session_token=12345; password=abcde` becomes `Cookie: session_token=[REDACTED]; password=[REDACTED]`)*

2. **HTTP Header Inspection & Token Generation:**
   The attacker used a specific request to trigger their backdoor. Inspect your redacted logs to find the single HTTP request that contains the custom header `X-Secret-Knock: open`. 
   Extract the `User-Agent` and the `X-Timestamp` header values from this specific request. 
   The attacker left behind a partial script `/home/user/evidence/verify_token.py`. Read this script to understand how the attacker generates their authentication token using the User-Agent and Timestamp. Write a Python script to compute the correct token for the attacker's request.

3. **Exploit/Payload Recovery:**
   The attacker encrypted the stolen data in `/home/user/evidence/stolen_data.enc`. They also left a decryption tool `/home/user/evidence/decrypt.py`. 
   Use the tool to decrypt the file by running:
   `python3 /home/user/evidence/decrypt.py --token <YOUR_GENERATED_TOKEN>`
   If successful, this will generate the file `/home/user/evidence/recovered.txt`.

4. **File Integrity Verification:**
   Compute the SHA-256 hash of `/home/user/evidence/recovered.txt`. Write ONLY the 64-character hex digest of the hash into a new file at `/home/user/evidence/hash.txt` (do not include the filename or any trailing newline in the hash file if possible, just the 64 characters).