You are a compliance analyst responding to a critical security audit. Several compiled binaries deployed in our web environment were found to contain hardcoded Social Security Numbers (SSNs), and our application's HTTP header configuration is missing a strict Content Security Policy (CSP).

Your task is to write a Python script at `/home/user/remediate.py` and run it to perform the required remediation.

The script must do the following:

1. **ELF Analysis & Redaction**:
   - Iterate through all files in the directory `/home/user/binaries/`.
   - For each file, determine if it is a valid ELF executable by checking its magic bytes (the first 4 bytes must be `\x7fELF`). Skip any file that is not a valid ELF file.
   - For valid ELF files, scan the binary content for any Social Security Numbers matching the exact pattern `XXX-XX-XXXX` (where `X` is a digit, i.e., `\d{3}-\d{2}-\d{4}`).
   - Redact these sensitive strings in-place within the binary by overwriting them exactly with `***-**-****`. (Do not change the file size or other binary structures).

2. **Audit Logging**:
   - For every valid ELF file processed, append an audit entry to `/home/user/audit.log`.
   - The log lines must be formatted exactly as: `[AUDIT] Processed <filename>: redacted <N> secrets.` (where `<filename>` is just the name of the file, not the full path, and `<N>` is the number of SSNs redacted).

3. **Content Security Policy Enforcement**:
   - There is a web server header configuration file at `/home/user/headers.conf`.
   - The script must read this file. If the file does not already contain a `Content-Security-Policy` directive, append the following exact line to the end of the file:
     `Content-Security-Policy: default-src 'self';`

Write and execute your script. You must complete the task such that the binaries are properly redacted, the audit log is generated, and the header config is secured.