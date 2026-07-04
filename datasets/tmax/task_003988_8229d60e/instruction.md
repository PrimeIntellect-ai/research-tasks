You are a compliance analyst investigating an open redirect vulnerability in our organization's legacy authentication server. As part of our new audit trail initiative, you need to build a high-performance shell script that acts as an audit filter for redirect payloads.

First, you have been provided with a scanned compliance memo located at `/app/memo.png`. This memo contains the single authorized, approved domain for user redirects. You will need to extract this domain (e.g., using a tool like `tesseract`). 

Next, write a Bash script at `/home/user/auditor.sh` that will process incoming redirect payloads to enforce strict Content Security Policy (CSP) rules and detect open redirects. The script must take exactly one argument: a Base64-encoded payload representing the intended redirect URL.

Your script must implement the following logic exactly, in order:
1. First, analyze the binary `/home/user/server.bin`. If the binary is NOT a 64-bit ELF executable (i.e., its ELF class is not ELF64), immediately print `AUDIT FAIL: SERVER BINARY INVALID` and exit with status 1. (Assume `readelf` or `file` is available).
2. Attempt to decode the provided Base64 argument. If the `base64 -d` command fails (returns a non-zero exit code), print `DECODE ERROR` and exit with status 0.
3. Check the decoded URL string. It must start exactly with `https://`. If it does not, print `INVALID PROTOCOL` and exit with status 0.
4. Extract the domain name from the decoded URL. The domain is the substring between the `https://` prefix and the very next forward slash `/`, or the end of the string if there is no trailing slash. 
5. Compare the extracted domain against the approved domain you found in `/app/memo.png`.
6. If the domain matches exactly, print the following CSP header to standard output:
   `SAFE - Content-Security-Policy: default-src 'none'; frame-ancestors https://<domain>;`
7. If the domain does NOT match, print:
   `OPEN REDIRECT ALERT: <domain>`

Requirements:
- Your script MUST handle standard base64 strings.
- Do NOT include any additional output, debug lines, or formatting. The output must be bit-exact to the specification.
- The script should be executable (`chmod +x /home/user/auditor.sh`).
- Use pure Bash (and standard coreutils like `readelf`, `base64`, `grep`, `awk`, `sed`) to ensure performance.