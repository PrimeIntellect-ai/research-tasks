You are a compliance analyst tasked with generating an automated security audit trail for a set of internal web services. 

The raw data from a recent security sweep has been dumped into `/home/user/audit_data/`. This directory contains two subdirectories:
1. `/home/user/audit_data/certs/`: Contains the TLS/SSL public certificates (PEM format) for various services. The files are named `<service_name>.pem`.
2. `/home/user/audit_data/responses/`: Contains the raw HTTP response headers (text format) captured from these services. The files are named `<service_name>.txt`.

Your task is to write a script (or set of scripts in bash, Python, Ruby, or Perl) that processes these artifacts and generates a consolidated JSON audit trail.

**Compliance Rules:**
1. **TLS/SSL Certificates**: 
   - Extract the "Issuer" Common Name (CN). If the Issuer does not have a CN, extract the Organization (O) name.
   - Extract the expiration date ("Not After") formatted strictly as `YYYY-MM-DD`.
2. **HTTP Headers**:
   - Check the HTTP response for the presence of the following required security headers (case-insensitive checking, but output exactly as written here): `Strict-Transport-Security`, `Content-Security-Policy`, and `X-Frame-Options`.
   - Record any of these three headers that are missing.
3. **Cookies**:
   - Inspect any `Set-Cookie` headers.
   - A cookie is considered non-compliant if it is missing either the `Secure` flag or the `HttpOnly` flag.
   - Record the names of any non-compliant cookies.

**Output Specification:**
Generate a JSON file at `/home/user/audit_trail.json` with the following structure:
```json
{
  "audit_results": [
    {
      "service": "<service_name>",
      "cert_issuer": "<Extracted Issuer CN or O>",
      "cert_expiry": "<YYYY-MM-DD>",
      "missing_headers": ["<header1>", "<header2>"],
      "non_compliant_cookies": ["<cookie_name>"]
    }
  ]
}
```
*Note:* The `audit_results` array should be sorted alphabetically by the `service` string. If there are no missing headers or non-compliant cookies, output empty arrays `[]` for those fields.

Process all services found in the `/home/user/audit_data/` directory. You may use standard Linux tools (`openssl`, `grep`, `awk`) or write code using standard libraries to parse the files.