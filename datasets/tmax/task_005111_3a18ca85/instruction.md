You are acting as a penetration tester and security auditor for a web application deployment. The application files are located in `/home/user/app/`. You have been provided with a checksum manifest file at `/home/user/manifest.txt` containing the original SHA-256 hashes of the application files.

Your objectives are:

1. **Integrity Check**: Use standard bash utilities to verify the cryptographic hashes of the files in `/home/user/app/` against `/home/user/manifest.txt`. Exactly one file has been tampered with by a malicious actor.
2. **CWE Identification**: Analyze the tampered source file to determine the vulnerability introduced. Identify the specific Common Weakness Enumeration (CWE) ID (e.g., CWE-89 for SQLi, CWE-79 for XSS, etc.) that best describes the flaw.
3. **Exploit Crafting**: The vulnerability allows for execution of arbitrary client-side scripts via a specific URL query parameter. Craft a minimal exploit payload that would trigger a JavaScript alert containing exactly the string `'pwned'` (i.e., popping an alert box with that exact string). Save only the payload string to `/home/user/payload.txt`.
4. **CSP Enforcement**: To mitigate the vulnerability at a defense-in-depth level, you must update the application's Content Security Policy. The CSP is defined in `/home/user/app/config.json`. Edit this file to change the `Content-Security-Policy` header value so that `default-src` is strictly set to `'self'` and any overly permissive directives (like `*` or `'unsafe-inline'`) are removed.
5. **Reporting**: Create a final audit report at `/home/user/audit_report.txt` with exactly the following format:
```
TAMPERED_FILE: /home/user/app/<filename>
CWE_ID: CWE-<number>
```
Replace `<filename>` with the name of the modified file, and `<number>` with the identified CWE number.

Do not use any external network requests or install new packages. Rely on standard built-in CLI tools (like `sha256sum`, `grep`, `sed`, `awk`, etc.).