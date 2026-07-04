You are a security auditor tasked with evaluating a local application environment. 

The application is stored in `/home/user/app`. A local development server is also running on `localhost:8080`. 

Your objective is to write a Go program at `/home/user/audit.go` that performs a security audit and outputs its findings to a JSON file at `/home/user/report.json`.

The Go program must perform the following checks:
1. **Privilege Escalation & File Permission Audit:**
   Recursively scan the `/home/user/app` directory. 
   - Identify any files that have the SUID bit set.
   - Identify any files that are world-writable (the 'others' write permission bit is set).

2. **Service & Content Security Policy (CSP) Audit:**
   - Send an HTTP GET request to `http://localhost:8080/`.
   - Check if the HTTP response includes the `Content-Security-Policy` header.

Your Go program should output a JSON file at `/home/user/report.json` with the exact following structure:
```json
{
  "suid_files": [
    "/absolute/path/to/file1",
    "/absolute/path/to/file2"
  ],
  "world_writable_files": [
    "/absolute/path/to/file3"
  ],
  "csp_enforced": true
}
```
*Note: The file paths in the arrays must be absolute paths. If no files are found for a category, use an empty array `[]`. `csp_enforced` should be `true` if the header is present and not empty, and `false` otherwise. The string arrays should be sorted alphabetically.*

Once you have written `/home/user/audit.go`, compile and run it so that `/home/user/report.json` is generated.