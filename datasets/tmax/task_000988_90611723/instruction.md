You are a compliance analyst generating audit trails for a legacy system. During an audit, you discovered a stripped binary at `/app/legacy_auditor`. This tool is used in production to validate proprietary access tokens (which are structurally similar to JSON Web Tokens) and generate compliance logs. 

Security audits have indicated that this binary suffers from a critical vulnerability: it completely bypasses signature validation if the token header specifies `"alg": "none"`, leading to potential privilege escalation if an attacker fabricates an `"admin": true` claim. Additionally, the binary scans token payloads for specific Injection and XSS vulnerability patterns, flagging them in its output.

Your task is to reverse-engineer `/app/legacy_auditor` and write a fully functionally equivalent Python script at `/home/user/py_auditor.py`. Your script must replicate the binary's exact logic, including its payload encoding/decoding mechanisms, its exact privilege escalation vulnerability (for accurate audit replication), and the precise injection payload signatures it detects.

Requirements:
1. Analyze `/app/legacy_auditor` (using tools like `strings`, `ltrace`, `strace`, `objdump`, or `gdb` which are available).
2. Create `/home/user/py_auditor.py` taking a single command-line argument (the token string).
3. The Python script must print exactly the same standard output as the binary for any given token input. Ensure whitespace, JSON keys, and boolean representations match perfectly.
4. Do not fix the vulnerabilities! You must faithfully replicate the binary's behavior, flaws and all, so we can use your script as a drop-in replacement for offline log analysis.

The system will verify your solution by randomly fuzzing both `/app/legacy_auditor` and your `py_auditor.py` with thousands of synthesized tokens to ensure bit-exact equivalence of the output.