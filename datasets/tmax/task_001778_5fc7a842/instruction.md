You are a security engineer responsible for rotating credentials and enforcing new security policies for an internal data processing service.

Your task consists of the following stages:

1. **Passphrase Recovery (Fixture Analysis):**
   A scanned image of the legacy hardware token's display is located at `/app/legacy_token.png`. Extract the text from this image (you may use `tesseract` which is installed on the system). This text is the legacy master passphrase.

2. **TLS Certificate Management:**
   Using the recovered passphrase as the password for the private key, generate a new RSA 2048-bit private key and a self-signed X.509 certificate. 
   - Save the private key to `/home/user/certs/server.key`.
   - Save the certificate to `/home/user/certs/server.crt`.
   - The certificate must have the Common Name (CN) set to `secure-api.internal`.

3. **Authentication & CSP Validation Tool (C Programming):**
   Write a C program at `/home/user/auth_validator.c` and compile it to `/home/user/auth_validator`. 
   This tool will act as an offline log analyzer that simulates our authentication flow and CSP enforcement.
   
   The program must accept two command-line arguments:
   `./auth_validator <path_to_cert> <path_to_log_csv>`
   
   The input CSV file will have lines with the following format:
   `RequestID,ClientToken,CSP_Header`
   
   For each line, your C program must:
   a) Validate the `ClientToken`. A token is considered VALID if it is exactly 32 hexadecimal characters long.
   b) Enforce the Content Security Policy. The `CSP_Header` string is considered VALID if it strictly contains both `default-src 'self'` and `require-trusted-types-for 'script'`.
   c) Output a single line to `stdout` for each request in the format:
      `RequestID: <STATUS>`
      Where `<STATUS>` is `PASS` if both the token and the CSP header are VALID, and `FAIL` otherwise.

Ensure your C code is robust, handles memory safely, and correctly parses the CSV format. We will test your compiled `/home/user/auth_validator` against a large, hidden dataset of logs to measure its accuracy.