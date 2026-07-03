You are a forensics analyst recovering evidence from a compromised web server. The server suffered from an open redirect vulnerability in its login flow, which attackers exploited to capture user credentials. We have found a suspicious binary left on the system, which the attackers used to temporarily store the exfiltrated HTTP requests.

Your objective is to extract, decrypt, verify, and sanitize this stolen data.

Here is the information about the compromised host environment:
- Working directory: `/home/user/evidence/`
- Suspicious binary: `/home/user/evidence/malware.bin` (an ELF executable)
- Key file: `/home/user/evidence/key.txt` (contains a plaintext string)
- Integrity file: `/home/user/evidence/checksum.sha256` (contains the expected SHA-256 hash of the successfully decrypted log)

Please perform the following steps (you may use standard Linux tools and write short Python scripts):

1. **Extract**: The attackers hid the encrypted log inside a custom ELF section named `.exfil` in `malware.bin`. Extract the raw binary contents of this section.
2. **Decrypt**: The extracted data is encrypted using a repeating-key XOR cipher. The key is the exact string found in `key.txt` (excluding any trailing newlines if you read it via script, though it will just be a raw string). Decrypt the extracted section.
3. **Verify**: Calculate the SHA-256 hash of your decrypted data. It must exactly match the hash provided in `checksum.sha256`.
4. **Redact**: The decrypted log contains stolen HTTP GET requests with sensitive parameters. You must redact the passwords. Find every instance of the URL parameter `password=` and replace its value with the exact string `REDACTED`. 
   - For example, `password=SuperSecret123&` should become `password=REDACTED&`. 
   - The password value ends at the next ampersand (`&`) or space character (` `).
5. **Save**: Save the final, redacted text to `/home/user/evidence/clean_log.txt`.

Ensure your final `clean_log.txt` accurately reflects the redaction without altering any other parts of the requests.