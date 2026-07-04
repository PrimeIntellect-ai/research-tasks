As a compliance analyst, you are responsible for maintaining our audit trails for a legacy file upload handler. We have a compiled executable located at `/app/legacy_audit_processor` that processes raw upload logs from standard input and prints a formatted, secure audit trail entry to standard output. 

Unfortunately, the original C source code for this processor was lost. Because this binary is old and hard to maintain, we need to port it to Python. 

Your task is to create a Python script at `/home/user/audit_processor.py` that is bit-for-bit equivalent to the behaviour of `/app/legacy_audit_processor`.

Through historical documentation, we know the processor does three things:
1. **Sensitive Data Redaction:** It finds standard US Social Security Numbers (SSNs) in the log text and redacts them.
2. **CWE Identification:** It looks for common path traversal sequences (CWE-22) typical in file upload exploits. If detected, it flags the log entry by prepending a specific alert tag.
3. **Cryptographic Checksum:** It computes a cryptographic hash of the processed log line and appends it to the output, separated by a specific character.

Since you don't have the source code, you will need to interact with the stripped binary `/app/legacy_audit_processor`, feed it various test inputs (normal text, text with SSNs, text with path traversal attempts), and observe its exact output format. 

Requirements:
- Your script must be located at `/home/user/audit_processor.py`.
- It must read a single string from standard input (`stdin`), process it, and print the exact same output to standard output (`stdout`) as the legacy binary would.
- It must perfectly match the redaction format, the exact CWE-22 alert string, the hashing algorithm, and the output delimiter used by the oracle.