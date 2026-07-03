You are a compliance analyst responsible for generating secure audit trails for our organization's authentication endpoints. We recently discovered that our legacy authentication worker—a stripped compiled binary located at `/app/legacy_auth_worker`—is vulnerable. Specifically, it leaks sensitive credentials as command-line arguments (visible in `/proc`) when it attempts to parse malformed HTTP cookies, and it improperly validates certificate chain checksums on certain compliance tokens.

Your task is to write a Python-based filter and audit script (`/home/user/auditor.py`) that acts as a strict pre-processor for this binary. 

You must analyze the legacy binary (tools like `strings`, `objdump`, or `gdb` are available) to understand exactly what triggers the vulnerability. The binary expects to read a JSON payload from standard input containing:
- `headers`: A dictionary of HTTP headers (including `Cookie`).
- `cert_chain`: A list of base64-encoded PEM certificates.
- `compliance_token`: A custom token string that includes a cryptographic checksum.

Your Python script `/home/user/auditor.py` must take a single command-line argument representing a directory containing these JSON payloads. It must process every `.json` file in the directory and write a final audit log to `/home/user/audit_trail.log`.

For each file, your script must:
1. Verify the certificate chain validates properly (e.g., signatures match down the chain).
2. Validate the compliance token's cryptographic checksum.
3. Inspect the HTTP headers and cookies to ensure they do not contain the specific malformed structures that cause the `/app/legacy_auth_worker` to leak credentials or crash.
4. If a file is completely safe and valid, log it as `ACCEPT`. If it violates any security constraints or triggers the binary's vulnerability, log it as `REJECT`.

The audit log at `/home/user/audit_trail.log` must have exactly this format, one line per file, sorted alphabetically by filename:
`[ACCEPT] /path/to/directory/file1.json`
`[REJECT] /path/to/directory/file2.json`

Ensure your script is robust. We will run it against two directories: a clean corpus of valid requests that must all be ACCEPTED, and an adversarial corpus of malicious requests that must all be REJECTED.