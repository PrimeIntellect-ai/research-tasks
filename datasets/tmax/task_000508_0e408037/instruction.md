You are a security auditor tasked with analyzing HTTP traffic for an older system to identify unauthorized access attempts and to securely redact sensitive credentials before releasing the logs.

Your tasks:
1. **Fix the HTTP Parser**: You are provided with the source code for a vendored HTTP parsing library, `picohttpparser` (v2.1), located at `/app/picohttpparser-2.1`. The previous auditor mentioned the source tree is slightly corrupted and fails to compile into an object file. Diagnose and fix the perturbation in the vendored package so it can be compiled and used.

2. **Reverse Engineer Legacy Auth**: The system uses a proprietary authorization mechanism. You are provided with an ELF executable `/app/legacy_auth`. This binary validates a hardcoded master admin token. The token is not visible using simple `strings` as it is constructed dynamically at runtime. Use reverse engineering/disassembly tools (e.g., `objdump`, `gdb`, `radare2`) on `/app/legacy_auth` to deduce the exact 16-character master admin token string.

3. **Traffic Analysis and Redaction (C++)**: 
   Write a C++ program at `/home/user/auditor.cpp` that compiles and links against your fixed `picohttpparser`. Your program must:
   - Read a raw HTTP traffic dump from `/app/traffic.raw`.
   - Parse each HTTP request (method, path, headers).
   - Inspect the headers (specifically `Authorization` and `Cookie`) for the presence of the master admin token you reversed in Step 2.
   - Reconstruct the raw HTTP traffic and write it to `/home/user/sanitized_traffic.raw`. In this output file, **every instance** of the master admin token must be exactly replaced with the literal string `[REDACTED]`.
   - For every request targeting the path `/admin` that does *not* contain the master admin token in its headers/cookies, log the line `UNAUTHORIZED: <Path>` to `/home/user/alerts.log`.

**Constraints & Verification**:
- You must use C++ for the parsing and redaction logic.
- Do not use external libraries other than the standard library and the provided `/app/picohttpparser-2.1`.
- Your final output `/home/user/sanitized_traffic.raw` will be scored by an automated metric evaluator based on Redaction Accuracy (100% of master tokens must be redacted, with no false positive redactions of other text). 
- To compile the parser, you typically just need to fix the source and run `gcc -c picohttpparser.c`.