You are a compliance analyst responsible for auditing application logs and generating sanitized audit trails. 

You have been given a log of raw HTTP response headers extracted from a legacy web server, located at `/home/user/http_dump.txt`. You need to perform a security audit and redact sensitive information using Bash command-line tools (like `grep`, `awk`, `sed`, etc.).

**Part 1: Vulnerability Auditing**
You must analyze the headers for specific security weaknesses and generate an audit report at `/home/user/vuln_audit.tsv`.
1. **CWE-614 (Insecure Cookies):** Find all `Set-Cookie` headers that lack the `Secure` attribute (exact case). 
2. **CWE-327 (Broken Crypto / ECB Mode):** Find all `X-Crypto-Payload` headers. These headers contain a lowercase hex string. You must perform a basic cryptanalysis check for ECB mode: flag any payload where the exact same 16-character block of hex digits repeats anywhere else within the same payload string.

Create a Tab-Separated Values (TSV) file at `/home/user/vuln_audit.tsv` containing the line numbers and the corresponding CWE ID for any vulnerable headers. 
The format must be: `<Line_Number>\t<CWE_ID>`. Sort the output numerically by line number.

**Part 2: Sensitive Data Redaction**
Generate a sanitized version of the log at `/home/user/redacted_dump.txt`. 
Apply the following redaction rules to the original `/home/user/http_dump.txt`:
1. For any `Set-Cookie:` header containing a `session=` directive, replace its alphanumeric value with the exact string `REDACTED`. (e.g., `Set-Cookie: session=abc123;` becomes `Set-Cookie: session=REDACTED;`).
2. For any `Authorization:` header using the `Bearer` scheme, replace the alphanumeric token with the exact string `REDACTED`. (e.g., `Authorization: Bearer secret99` becomes `Authorization: Bearer REDACTED`).
All other lines and header content must remain completely unchanged.