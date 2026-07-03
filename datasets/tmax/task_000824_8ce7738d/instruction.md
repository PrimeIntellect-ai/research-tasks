You are acting as a security auditor responding to a recent path traversal vulnerability in a file upload handler. Attackers may have leaked or uploaded sensitive SSH private keys into the public uploads directory.

Your task is to write a Go program at `/home/user/audit_keys.go` that recursively scans the `/home/user/uploads` directory to identify, redact, and secure any exposed SSH private keys.

Requirements for `/home/user/audit_keys.go`:
1. Recursively search `/home/user/uploads` for any files containing the exact string `-----BEGIN OPENSSH PRIVATE KEY-----`.
2. For every file containing this string:
   a. **Redact the content:** Replace all text between the `-----BEGIN OPENSSH PRIVATE KEY-----` header and the `-----END OPENSSH PRIVATE KEY-----` footer with exactly `\n[REDACTED]\n`. Ensure the header and footer remain intact. Overwrite the file with this new content.
   b. **Fix permissions:** Change the file's permissions to `0600` (read and write for the owner only).
   c. **Log the action:** Append the absolute path of the modified file to `/home/user/audit_log.txt`.
3. The final `/home/user/audit_log.txt` must contain a sorted list (alphabetical, ascending) of the absolute paths of all modified files, with one path per line. 

Ensure your Go code can be executed simply via `go run /home/user/audit_keys.go`. You are allowed to use standard Go libraries only.