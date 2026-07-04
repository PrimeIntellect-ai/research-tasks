You are a compliance analyst tasked with generating an automated security audit trail for a legacy application endpoint. 

The application is deployed at `/home/user/app/legacy_endpoint`. This is an ELF binary. 
As part of our compliance process, we must audit the hardcoded configurations inside this binary, validate its associated certificate chain, and test its intrusion detection mechanism against a sample traffic log.

You must write a C program named `/home/user/compliance_auditor.c` (and compile it to `/home/user/compliance_auditor`) that performs the following steps to generate a final audit report at `/home/user/audit_trail.txt`.

Requirements for your C program:
1. **ELF Analysis:** The binary `/home/user/app/legacy_endpoint` contains a custom ELF section named `.audit_config`. Extract the contents of this section. It contains a semicolon-separated string with two key-value pairs: `AUTH_TOKEN=<token>;IDS_PATTERN=<regex>`.
2. **Certificate Validation:** The application uses a certificate at `/home/user/app/server.crt` with a root CA at `/home/user/app/ca.crt`. Your program must programmatically validate this certificate chain (you may use `system()` or `popen()` with standard CLI tools like `openssl` to perform the validation).
3. **Authentication Flow & IDS Pattern Matching:** A sample traffic capture is located at `/home/user/app/traffic.log`. Using the `IDS_PATTERN` extracted from the ELF binary, use POSIX regular expressions (`<regex.h>`) in your C program to scan the `traffic.log` file line by line. Count the number of lines that match the intrusion detection pattern.

Output formatting for `/home/user/audit_trail.txt`:
Your C program must generate a file exactly matching this format:
```
[AUDIT REPORT]
AUTH_TOKEN: <extracted_token>
CERT_STATUS: <VALID or INVALID>
IDS_MATCHES: <number_of_matching_lines>
```

Notes:
- You may install any necessary C development libraries (like `libelf-dev` or `build-essential`) using `sudo apt-get` if they are not present, although invoking `objdump` via `popen` in C is also acceptable for ELF extraction.
- The `CERT_STATUS` should be `VALID` if the OpenSSL verification succeeds, and `INVALID` otherwise.