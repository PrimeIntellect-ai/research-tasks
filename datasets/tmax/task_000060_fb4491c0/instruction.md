You are a compliance analyst building an automated audit trail verifier for a secure CI/CD pipeline. Your team intercepts compiled binaries, hex-encodes them for safe transport, and logs them. You need to write a standalone classifier to determine if these logged payloads should be accepted or rejected based on strict security rules.

An image of the master compliance certificate is located at `/app/auditor_cert.png`. You must extract the master compliance token from this image (e.g., using `tesseract`). 

Your task is to create a Rust CLI application in `/home/user/audit_filter` that acts as the admission controller.

**Requirements for the Rust application:**
1. **Entry Point**: The program must compile to `/home/user/audit_filter/target/release/audit_filter` and accept exactly one argument: the path to a payload file.
2. **Payload Decoding**: The input files contain a plain-text hex string representing an ELF binary. Your program must decode this hex payload into raw bytes.
3. **Token Validation**: The program must scan the raw decoded bytes for the master compliance token extracted from the image. If the token is missing, the payload must be rejected.
4. **CWE Identification**: The program must audit the decoded bytes for common vulnerability patterns often embedded by malicious actors (CWE-89 and CWE-79). If the payload contains any of the following literal strings, it must be rejected:
   - `UNION SELECT`
   - `' OR '1'='1`
   - `javascript:`
   - `onerror=`
5. **Exit Codes**: The program must exit with code `0` (Accept) if the token is present AND no vulnerability strings are found. It must exit with code `1` (Reject) if the token is missing OR any vulnerability string is found.

**Test Data:**
You have been provided with two directories containing hex-encoded payloads:
- `/app/corpus/clean/` (Valid payloads that follow all rules)
- `/app/corpus/evil/` (Malicious or non-compliant payloads)

Initialize your Rust project, write the validation logic, build it in release mode, and ensure it correctly classifies the provided corpora. Do not hardcode file paths from the corpus in your source code; it must operate strictly on the file path passed via CLI.