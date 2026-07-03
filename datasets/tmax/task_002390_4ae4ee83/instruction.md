You are a web security engineer responsible for rotating credentials and securing our legacy infrastructure. Recently, a vulnerability scan flagged our custom credential rotation service for potential path traversal, but the original source code is lost. 

We only have the compiled, stripped binary located at `/app/cred_rotator`.

The service listens for incoming HTTP POST requests and uses a custom header, `X-Cred-Path:`, to determine where to save the rotated credentials within the `/etc/creds/` directory.

Your task:
1. Reverse engineer the stripped binary at `/app/cred_rotator` to identify how it parses the `X-Cred-Path` header and discover the exact path traversal vulnerability. Pay close attention to any character replacements, URL decoding, or sanitization steps it performs.
2. Write a request classifier/WAF script at `/home/user/waf.sh`.
3. Your script must accept exactly one argument: the path to a file containing a raw HTTP request.
4. The script must exit with status `0` if the `X-Cred-Path` is benign and safe.
5. The script must exit with status `1` if the request attempts to exploit the specific path traversal vulnerability you identified in the binary.
6. Make sure your script handles standard inputs properly and accurately models the binary's parsing flaws to prevent bypasses and false positives.

You may write `/home/user/waf.sh` in bash, Python, or any other standard language available on the system. Ensure it is executable.