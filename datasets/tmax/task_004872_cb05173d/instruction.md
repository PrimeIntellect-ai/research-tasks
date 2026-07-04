You are a DevSecOps engineer enforcing policy as code for a data processing pipeline. Your team has a Go utility that is supposed to validate an incoming entity's X.509 certificate against a trusted root CA, and if valid, process their transaction log by redacting sensitive data (Credit Card numbers). 

However, the current script at `/home/user/buggy_checker.go` is insecure and incomplete. It fails to properly validate the certificate chain, exposing the system to Man-in-the-Middle (MitM) or spoofing attacks, and it completely misses the redaction step.

Your task is to:
1. **Identify the vulnerability:** Audit `/home/user/buggy_checker.go`. Identify the specific CWE identifier for the certificate validation vulnerability present in the code. Write the exact CWE ID (e.g., `CWE-123`) to `/home/user/cwe.txt`.
2. **Fix the code:** Write a corrected version of the Go program to `/home/user/fixed_checker.go`. 
    - The program must accept three command-line arguments: `<leaf_cert.pem> <root_cert.pem> <log_file.txt>`.
    - It must properly load the provided `<root_cert.pem>` into an `x509.CertPool`.
    - It must parse `<leaf_cert.pem>` and securely verify that it is signed by the provided root CA and is valid for the DNS name `secure.internal.com`.
    - If certificate verification fails, the program must print an error and exit with a non-zero status code.
    - If verification succeeds, the program must read the file at `<log_file.txt>`.
    - It must redact all 16-digit credit card numbers formatted exactly as `DDDD-DDDD-DDDD-DDDD` (where `D` is a digit). Replace the entire 19-character string with `XXXX-XXXX-XXXX-XXXX`.
    - The program must print the redacted log content to standard output.
3. **Execute the pipeline:** Run your fixed program using the files provided in the environment:
    - Leaf certificate: `/home/user/certs/leaf.pem`
    - Root certificate: `/home/user/certs/root.pem`
    - Log file: `/home/user/logs/transactions.log`
    
    Save the standard output of your fixed program to `/home/user/redacted_output.log`.

Ensure your Go code is well-formed, handles errors gracefully, and strictly meets the redaction and validation requirements.