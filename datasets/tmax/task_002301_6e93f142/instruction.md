You are a network security engineer inspecting a custom C-based traffic analysis proxy. Your team uses this proxy to analyze raw HTTP responses, enforce security headers, and redact sensitive data before passing it to internal logging systems. 

However, the current version of the proxy source code (`/home/user/traffic_inspector.c`) has multiple issues:
1. **CWE Vulnerability:** The C code contains a buffer overflow vulnerability when copying the HTTP payload. 
2. **Broken Redaction:** The redaction logic is supposed to find any occurrence of `SSN: ` followed by a 11-character social security number (e.g., `SSN: 123-45-6789`) and replace the 11-character number entirely with `REDACTED!!!`. Currently, the logic is flawed and doesn't fully redact the data.
3. **Missing CSP:** The proxy is supposed to prepend a Content-Security-Policy header to the inspected payload, but this feature is missing.

Additionally, you have been provided with an older compiled ELF binary of the proxy (`/home/user/legacy_inspector`). Your team lost the source code for this specific build, but you know it contains a hardcoded staging Certificate Authority (CA) URL used for chain validation testing.

Perform the following tasks:

1. **Binary Analysis:** Analyze the ELF binary `/home/user/legacy_inspector` to find the hardcoded staging CA URL (it starts with `https://staging-ca.`). Write the exact URL to `/home/user/hidden_ca.txt`.
2. **Code Auditing & Fixes:** Edit `/home/user/traffic_inspector.c` to:
   - Fix the buffer overflow vulnerability (ensure safe string copying).
   - Fix the sensitive data redaction logic so it properly replaces the 11-character SSN with `REDACTED!!!`.
   - Prepend the string `Content-Security-Policy: default-src 'self'\n` to the final output buffer before printing it.
3. **Compilation:** Compile your fixed code to `/home/user/fixed_inspector` using `gcc`.
4. **Execution:** Run your fixed binary and feed it the file `/home/user/raw_traffic.txt`. Redirect the standard output to `/home/user/safe_traffic.txt`.

Ensure your C program reads from standard input or a file, and prints the secured, redacted payload to standard output.