You are a compliance analyst tasked with generating an audit trail for a legacy application's offline request processor. An external audit revealed that the current system fails to validate client certificates properly, lacks basic intrusion detection, and contains a critical vulnerability where it accepts JWT-like authorization tokens using the insecure `alg: none` method.

Your objective is to build an automated auditing tool in C, generate a proper Public Key Infrastructure (PKI) environment for testing, and produce a final compliance report.

Step 1: TLS/SSL Certificate Management
Create a directory `/home/user/certs/`. Using OpenSSL, generate the following certificate chain:
1. A self-signed Root CA (`rootCA.pem` and `rootCA.key`).
2. An Intermediate CA (`intermediateCA.pem` and `intermediateCA.key`) signed by the Root CA.
3. Concatenate them into a single chain file at `/home/user/certs/ca-chain.pem`.
4. Generate a valid client certificate (`client_valid.pem` and `client_valid.key`) signed by the Intermediate CA.
5. Generate an untrusted client certificate (`client_invalid.pem`) signed by a completely different, newly generated dummy Root CA.

Step 2: Secure Auditing Tool Development
Write a C program at `/home/user/audit_tool.c` that takes exactly two command-line arguments:
`./audit_tool <request_file_path> <client_cert_path>`

The program must perform the following tasks in order:
1. **Certificate Chain Validation:** Use the OpenSSL library in C to verify the provided `<client_cert_path>` against the trusted chain at `/home/user/certs/ca-chain.pem`. If validation fails, the program must print `AUDIT: [REJECT] Cert invalid` to standard output and exit.
2. **Token Vulnerability Analysis:** Read the `<request_file_path>`. The file contains HTTP-like plaintext. Find the line starting with `Authorization: Bearer `. The token consists of three dot-separated Base64Url encoded strings (`header.payload.signature`). Decode the header part. If the decoded JSON contains `"alg":"none"`, print `AUDIT: [REJECT] Insecure algorithm` and exit.
3. **Intrusion Detection:** Scan the entire contents of `<request_file_path>` (including headers and body). If the exact substring `<script>` is found anywhere, print `AUDIT: [REJECT] XSS detected` and exit.
4. If the certificate is valid, the algorithm is not "none", and no XSS payload is found, print `AUDIT: [PASS] Request accepted` and exit.

Compile your tool to `/home/user/audit_tool`. Ensure you link the necessary OpenSSL libraries (`-lssl -lcrypto`).

Step 3: Generating the Audit Trail
Write a bash script at `/home/user/run_audit.sh` that creates four simulated request files in `/home/user/requests/`:
- `req1.txt`: Contains a valid header `Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.payload.sig` and safe body.
- `req2.txt`: Contains an insecure header `Authorization: Bearer eyJhbGciOiJub25lIn0.payload.sig` and safe body.
- `req3.txt`: Contains a valid header but the body contains `<script>alert(1);</script>`.
- `req4.txt`: Contains a valid header and safe body.

The script must run `./audit_tool` and append the results to `/home/user/audit_trail.log` in exactly this format for each test:
```
Test 1:
[OUTPUT OF AUDIT TOOL WITH req1.txt and client_invalid.pem]
Test 2:
[OUTPUT OF AUDIT TOOL WITH req2.txt and client_valid.pem]
Test 3:
[OUTPUT OF AUDIT TOOL WITH req3.txt and client_valid.pem]
Test 4:
[OUTPUT OF AUDIT TOOL WITH req4.txt and client_valid.pem]
```

Run your script so that `/home/user/audit_trail.log` is generated successfully.