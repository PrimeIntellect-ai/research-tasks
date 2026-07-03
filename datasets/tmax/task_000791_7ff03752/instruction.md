You are a DevSecOps engineer working on modernizing our policy-as-code infrastructure. We have an old, undocumented, stripped binary located at `/app/legacy_audit` that evaluates security configurations (like HTTP headers, CSP directives, and file permission bits) and generates a cryptographic policy compliance signature. 

Unfortunately, the source code for `/app/legacy_audit` was lost. Your task is to reverse-engineer this binary and write a bit-exact equivalent program in C.

The binary takes a single command-line argument (a string representing the security configuration) and outputs a signature and some flags based on its inspection of the string.

Requirements:
1. Analyze the `/app/legacy_audit` binary to understand its logic. It performs a custom hashing algorithm on the input and checks for the presence of specific substrings related to Content Security Policy, Secure cookies, and ports.
2. Write a C program at `/home/user/audit_rewrite.c` that exactly replicates the behavior of the legacy binary for ANY given input string.
3. Compile your program to `/home/user/audit_rewrite`. We will use an automated fuzzer to pass thousands of random inputs to both `/app/legacy_audit` and `/home/user/audit_rewrite` and assert that their standard output and exit codes are identical in every case.

Ensure your compiled binary does not crash on empty inputs or extremely long strings, matching the exact memory safety (or lack thereof) of the original binary if applicable (assume the original bounds-checks up to 1024 bytes, but you should verify this).