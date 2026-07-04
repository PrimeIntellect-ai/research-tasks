You are acting as a penetration tester auditing a multi-language internal web application. You have been given access to the application source code and configuration scripts located in `/home/user/app`.

Your task involves three objectives:

1. **Code Auditing & CWE Identification**: 
   Inspect the file `/home/user/app/api.php`. It contains a severe vulnerability. Identify the standard CWE (Common Weakness Enumeration) identifier for this vulnerability (format: `CWE-XXX`).

2. **Cookie Inspection**:
   Inspect the file `/home/user/app/auth.py`. The `set_cookie` function is missing standard security flags that protect cookies from client-side script access and unencrypted transit. Identify these missing flags.

3. **TLS/SSL Certificate Management**:
   The script `/home/user/app/gen_cert.sh` is used to generate self-signed certificates for the development server. However, it currently uses dangerously weak cryptographic parameters (a weak RSA key size and a deprecated hashing algorithm). 
   Modify `/home/user/app/gen_cert.sh` to use an RSA key size of `2048` bits and the `sha256` hashing algorithm. Leave all other parameters (like validity days and subject) unchanged. Once modified, execute the script to generate `server.key` and `server.crt` in `/home/user/app/`.

Finally, create a JSON report of your findings at `/home/user/findings.json` with the exact following structure:
```json
{
  "api.php": "CWE-XXX",
  "auth.py_missing_flags": ["Flag1", "Flag2"]
}
```
*Note: Sort the missing cookie flags alphabetically in the JSON array.*