You are a compliance analyst tasked with generating an automated security audit trail for a newly deployed application package. You need to inspect the application's binary, its SSL certificates, and its HTTP security headers to ensure they meet our baseline security compliance requirements.

All the files you need to audit are located in the `/home/user/audit_target/` directory:
1. `app_bin` - The main application executable.
2. `root.pem`, `intermediate.pem`, `leaf.pem` - The certificate chain provided for the application.
3. `headers.txt` - A text file containing the HTTP headers returned by the application.

Your task is to analyze these components and generate an audit report at `/home/user/audit_report.txt` with the following strict format:

```
[AUDIT TRAIL]
Binary_Machine: <Machine type from readelf>
Cert_Status: <VALID|INVALID>
CSP_Status: <ENFORCED|MISSING>
```

**Instructions for the checks:**
1. **Binary_Machine**: Use `readelf -h` on the `app_bin` and extract the exact string value of the `Machine:` field (trim leading spaces, but keep the exact text, e.g., "Advanced Micro Devices X86-64").
2. **Cert_Status**: Use `openssl verify` to validate the `leaf.pem` certificate using `root.pem` as the trusted CA and `intermediate.pem` as the untrusted intermediate. If the verification succeeds (returns OK), output `VALID`. Otherwise, output `INVALID`.
3. **CSP_Status**: Inspect `headers.txt`. If the `Content-Security-Policy` header is present AND strictly contains the directive `default-src 'none'` (case-sensitive, exact substring match), output `ENFORCED`. Otherwise, output `MISSING`.

Complete the task using standard shell commands or a short script of your choice. Ensure the final report file is saved at exactly `/home/user/audit_report.txt`.