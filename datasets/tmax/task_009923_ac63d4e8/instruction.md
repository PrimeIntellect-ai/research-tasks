You are a security auditor reviewing the permissions and integrity of a legacy web application. 

You need to analyze the files in the directory `/home/user/webapp/` to identify insecurely modified files and categorize the introduced vulnerabilities. 

Write a script (in bash, python, or your preferred language) to perform the following audit:
1. Find all files in `/home/user/webapp/` that are world-writable (i.e., others have write permissions).
2. For those world-writable files, compute their SHA-256 checksums and compare them to the original known-good hashes listed in `/home/user/webapp/checksums.txt`.
3. If a world-writable file's hash does **not** match the hash in `checksums.txt`, analyze its contents to categorize the security risk:
   - If the file contains the exact string `eval(` or `innerHTML =`, categorize it as `XSS`.
   - If the file contains the string `Content-Security-Policy` AND the string `'unsafe-inline'`, categorize it as `CSP`.
   - If it contains neither, you can ignore it.

Finally, generate an audit report at `/home/user/audit_results.csv` with the following format (including the exact header):
```csv
Filename,Vulnerability,Current_SHA256
```
Where `Filename` is just the base name of the file (e.g., `index.html`), `Vulnerability` is either `XSS` or `CSP`, and `Current_SHA256` is the actual, newly computed SHA-256 hash of the modified file.

Sort the CSV alphabetically by `Filename` (ignoring the header).