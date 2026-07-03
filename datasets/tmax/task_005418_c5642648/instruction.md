You are a red-team operator attempting to bypass a target's Web Application Firewall (WAF) using an evasion payload. During reconnaissance, you managed to exfiltrate a stripped ELF executable from the WAF's backend, located at `/app/waf_cookie_hasher`. 

This binary processes HTTP `Cookie` header strings, extracts a specific payload field, and computes a signature. To effectively conduct offline password cracking and brute-force search for an evasive payload without alerting the network's intrusion detection systems, you need a bit-exact replica of this hashing algorithm.

Your task is to analyze the stripped binary and write a C program that perfectly replicates its behavior. 

Requirements:
1. Reverse engineer the binary at `/app/waf_cookie_hasher` to understand its parsing logic and hashing algorithm.
2. Write a C program at `/home/user/replica.c`.
3. Compile it to `/home/user/replica`.
4. Your replica must accept a single command-line argument: the raw Cookie string (e.g., `./replica "session=xyz; payload=test; extra=1"`).
5. Your replica must produce the exact same standard output, standard error, and exit codes as the original binary for any given input string.

The verification system will aggressively fuzz both your compiled `/home/user/replica` and the original `/app/waf_cookie_hasher` with thousands of random HTTP cookie configurations to ensure they are strictly equivalent.