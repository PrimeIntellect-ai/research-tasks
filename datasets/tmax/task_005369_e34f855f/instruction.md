You are a forensics analyst tasked with recovering and sanitizing evidence from a compromised host. We have extracted an AES-256-CBC encrypted log dump from the host, located at `/app/evidence.enc`. 

Your objective is to create a C++ tool that decrypts this evidence, aggressively redacts sensitive Personally Identifiable Information (PII) using fast pattern matching, and securely stores the sanitized output.

Specifically, you must:
1. Fix and build the fast regular expression library `re2`, which we have vendored from source at `/app/re2`. The package seems to have a minor build misconfiguration preventing compilation. Fix the build system, compile it, and install it to a local prefix (e.g., `/home/user/local`).
2. Write a C++ program at `/home/user/redactor.cpp` that links against OpenSSL (for decryption) and your fixed `re2` library (for pattern matching).
3. Your C++ program must read and decrypt `/app/evidence.enc`.
   - Algorithm: AES-256-CBC
   - Key (Hex): `3132333435363738393061626364656631323334353637383930616263646566`
   - IV (Hex): `30303030303030303030303030303030`
4. Use `re2` to parse the decrypted log entries and redact the following PII by replacing the matched characters exactly with `X`s:
   - Social Security Numbers: Formatted exactly as `XXX-XX-XXXX` (where `X` is a digit).
   - Credit Card Numbers: Formatted as 16 digits, which may be contiguous or separated by hyphens (e.g., `1234567812345678` or `1234-5678-1234-5678`).
5. Write the redacted, decrypted log to `/app/clean_evidence.log`.
6. Ensure that the resulting file `/app/clean_evidence.log` has restrictive access controls applied: only the owner should have read and write permissions (`chmod 600`).

Ensure your redaction logic is highly accurate. An automated metric verifier will compute the F1 score of your redactions compared to the ground-truth PII locations in the raw log.