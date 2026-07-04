As a security auditor, you have been tasked with auditing a proprietary binary used in our infrastructure for checking privilege escalation tokens. The binary is located at `/app/priv_checker`. It is currently stripped and we lost the source code. 

Your task is to reverse-engineer `/app/priv_checker` and write a fully functionally equivalent Python script at `/home/user/priv_checker.py`.

We know the following about the binary:
- It takes exactly one argument: a base64-encoded payload string.
- Internally, it decodes the payload, performs a basic certificate chain validation (checking against `/app/certs/root.pem`), and extracts a Content Security Policy (CSP) string and a requested privilege level.
- It prints either "DENIED", "GRANTED: <priv_level>", or "ERROR: <reason>" to standard output.
- It exits with 0 on success, or non-zero on failure.

Your Python script `/home/user/priv_checker.py` must replicate the binary's behavior bit-for-bit for any arbitrary input string. We will test your script by generating thousands of random payloads and asserting that the standard output, standard error, and exit codes of your script match the original binary exactly.

Ensure your Python script is executable and has the appropriate shebang.