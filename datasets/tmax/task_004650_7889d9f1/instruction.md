You are a penetration tester who recently intercepted a set of authentication logs and certificate captures during an internal engagement. You need to prepare these logs for your final client report, which means you must sanitize them by redacting any cracked passwords and exposed private key data, while leaving valid public certificate chains and secure authentication attempts intact.

To do this, you will write a custom log sanitizer in C. You have been provided with a vendored password hashing library, `fastpbkdf2` (version 1.0.0), located at `/app/fastpbkdf2`.

However, the vendored package is currently broken. 
1. The `Makefile` inside `/app/fastpbkdf2` has a deliberate perturbation: the `CFLAGS` variable has been tampered with to include an invalid flag (`-Oinvalid`), which prevents compilation.
2. You must fix the `Makefile`, compile the library, and then write a C program at `/home/user/sanitizer.c`.

Your C program (`/home/user/sanitizer`) must read line-by-line from standard input and write to standard output. It must act as a filter/redactor with the following rules:

1. **Password Verification & Redaction:** 
   Log lines containing authentication attempts are formatted as: `AUTH user:<username> hash:<pbkdf2_sha256_hash> salt:<salt>`.
   You must use the fixed `fastpbkdf2` library to hash a known short dictionary of weak passwords (`password`, `123456`, `admin`). If the hash in the log matches one of these weak passwords (meaning it was successfully cracked), you must output the line exactly as: `AUTH user:<username> REDACTED`
   If the hash does NOT match any of the weak passwords, output the line unchanged.

2. **Certificate Data & Private Key Redaction:**
   The logs also contain PEM-encoded data.
   Any line containing `-----BEGIN PRIVATE KEY-----` or `-----BEGIN RSA PRIVATE KEY-----` indicates sensitive key material. You must drop/reject the entire block (do not output it) until the corresponding `-----END ... KEY-----` line is reached.
   Lines containing public certificate chains (`-----BEGIN CERTIFICATE-----` to `-----END CERTIFICATE-----`) must be preserved and output unchanged.

3. **General Logs:**
   Any other normal log lines must be output unchanged.

Compile your program into an executable at `/home/user/sanitizer`. You must link it dynamically or statically against the fixed `/app/fastpbkdf2` library.

An automated test will run your executable against two corpora:
- An "evil" corpus containing weak authentication hashes and private keys.
- A "clean" corpus containing strong hashes, regular logs, and public certificate chains.
Your program must successfully redact/reject 100% of the evil entries while preserving 100% of the clean entries.