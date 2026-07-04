You are a compliance analyst tasked with generating secure audit trails from a proprietary web server. The web server dumps raw, obfuscated logs. We have provided a stripped, closed-source binary tool at `/app/bin/log_decoder` which decodes these raw logs into plaintext. 

However, the plaintext logs often contain highly sensitive data (like accidentally leaked TLS private keys) and active exploit payloads (like XSS attacks in request parameters). For compliance, these must be redacted and cryptographically sealed before storage.

Your task is to create a C program, compiled to `/home/user/redactor`, that acts as a secure log filter. 

Requirements for `/home/user/redactor`:
1. It must read a single line of plaintext log from standard input (`stdin`).
2. **Sensitive Data Redaction**: If the line contains a leaked TLS private key (specifically, any substring matching the exact regex `-----BEGIN PRIVATE KEY-----.*?-----END PRIVATE KEY-----`), replace that entire matched substring with the exact string `[REDACTED_KEY]`.
3. **Intrusion Pattern Matching**: If the line contains an XSS exploit payload in a URL (specifically, any substring matching the regex `<script>.*?</script>`), replace that entire matched substring with the exact string `[MALICIOUS_PAYLOAD]`.
4. **Cryptographic Checksum**: After applying any necessary redactions, compute the SHA-256 hash of the resulting string (excluding the trailing newline). Append the hash to the end of the output in the format: ` | SHA256: <lowercase_hex_hash>`, followed by a newline. Output this final string to `stdout`.
5. Clean logs (which contain no private keys or script tags) must remain exactly as they are, with only the SHA-256 hash suffix appended.

We have provided two test corpora for your filter:
- `/app/corpora/clean/`: Contains normal web logs. Your program must preserve the log text identically (plus the appended hash).
- `/app/corpora/evil/`: Contains logs with embedded private keys and XSS payloads. Your program must successfully redact the sensitive portions (plus the appended hash).

You may use standard POSIX libraries (e.g., `<regex.h>`) and standard crypto libraries available on the system (e.g., OpenSSL's `<openssl/sha.h>`) to compile your C code. Ensure you compile your code to exactly `/home/user/redactor` (e.g., `gcc -O2 redactor.c -o redactor -lcrypto`).

Verify your work against the files in the corpora to ensure 100% compliance.