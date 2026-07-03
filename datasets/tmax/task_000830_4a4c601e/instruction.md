You are an incident responder investigating a series of mysterious crashes in a legacy authentication service. 

We have recovered the stripped binary of the service, located at `/app/token_checker`. This binary takes a single Base64-encoded token as a command-line argument, decodes it, and validates the internal payload. Security logs indicate that attackers are actively exploiting a vulnerability (CWE) in this token validation process to crash the service or potentially execute code. 

Your tasks:
1. Analyze the `/app/token_checker` stripped binary to identify the vulnerability. You can use standard tools like `gdb`, `strings`, `ltrace`, or simply use the binary as a black-box oracle to observe what inputs cause a segmentation fault.
2. Based on your CWE identification, write a C program `/home/user/detector.c` and compile it to `/home/user/detector`.
3. Your detector must act as a filter for incoming tokens. It should take a Base64-encoded token as its first command-line argument (`argv[1]`).
4. If the decoded token contains the malicious payload pattern targeting this specific vulnerability, the program must exit with status code `1` (Reject).
5. If the decoded token is benign, the program must exit with status code `0` (Accept).

Constraints:
- Do not rely on external libraries other than standard C libraries.
- The detector must catch the structural exploit payload, not just exact string matches.
- The binary does not require root privileges to run or analyze.

Write and compile the detector. An automated test suite will invoke your compiled `/home/user/detector` against a large corpus of both benign and malicious tokens.