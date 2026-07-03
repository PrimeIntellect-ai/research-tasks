You are a DevSecOps engineer tasked with implementing a strict "Policy-as-Code" validator for a web server's login flow. The server has been experiencing open redirect vulnerabilities and cookie tampering. 

Your objective is to write a standalone Python script at `/home/user/policy.py` that acts as a security filter. It will read a single JSON object from standard input (stdin) representing an HTTP request, and output exactly one line to standard output (stdout): either `ALLOW` or a specific `DENY` reason.

The JSON input will have the following schema:
`{"host": "example.com", "path": "/login?next=/dashboard", "cookie": "auth_sig=abc123def..."}`

You must implement the following security rules in strict order of precedence:

**1. Cryptographic Signature Validation (Cookie Inspection)**
The `cookie` field will always contain a string in the format `auth_sig=<hex_string>`.
This `<hex_string>` is the SHA-256 hex digest of the concatenated string: `host + path + secret_salt`.
We received an intercepted audio file from the legacy development team at `/app/voicemail.wav`. You must transcribe this audio to find the `secret_salt`. The speaker will say "The shared salt is [two words]". Those two words (lowercase, separated by a single space) are the exact `secret_salt`.
*If the signature does not perfectly match, your script must output: `DENY: INVALID_SIGNATURE`*

**2. Intrusion Detection Pattern Matching**
Extract the value of the `next` query parameter from the `path` (if it exists). 
If the `next` value contains the exact substrings `javascript:`, `data:`, or `../` (case-insensitive), it is an attack.
*If matched, your script must output: `DENY: MALICIOUS_PAYLOAD`*

**3. Open Redirect Prevention**
If the `next` query parameter exists, it must be validated. It is considered an open redirect if:
- It starts with `//` (protocol-relative URL to another domain).
- It is an absolute URL (starts with `http://` or `https://`), BUT the hostname extracted from this URL does not exactly match the `host` field from the JSON input.
*If it violates this rule, your script must output: `DENY: OPEN_REDIRECT`*

**4. Default Allow**
If all checks pass (or if there is no `next` parameter and the signature is valid), output: `ALLOW`

**Execution Requirements:**
- The script must be executable via `python3 /home/user/policy.py`.
- It must read from `sys.stdin` and print the result to stdout.
- It must handle URL-encoded characters in the `path` correctly when parsing query parameters.
- Do not print any debug information to stdout.