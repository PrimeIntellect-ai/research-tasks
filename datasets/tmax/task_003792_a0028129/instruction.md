You are a DevSecOps engineer enforcing policy-as-code for our microservices architecture, specifically focusing on mitigating open redirect vulnerabilities during authentication flows.

There are two parts to this task:

Part 1: Fix the Vendored Auth Package
We have vendored a third-party authentication utility package located at `/app/auth-redirect-v1.0.0`. Due to a bad backport, the package has a deliberate flaw in its URL validation logic (specifically, a missing patch in the host extraction logic in `auth.py` where it strips the port incorrectly, and a broken Makefile).
1. Inspect the source in `/app/auth-redirect-v1.0.0`.
2. Fix the bug in `auth.py` so that it correctly handles domains with or without ports. 
3. Fix the `Makefile` so that running `make test` inside `/app/auth-redirect-v1.0.0` successfully runs the test suite and returns exit code 0.

Part 2: Implement a Policy-as-Code Validator
We need a standalone executable utility that evaluates untrusted redirect URLs based on strict security rules. 
Create an executable script at `/home/user/validate_redirect` (it can be written in Python, Node.js, or Bash). 
It must accept exactly two positional command-line arguments:
`$1` = `allowed_base_domain` (e.g., `example.com`)
`$2` = `untrusted_url`

Your utility must implement the following logic:
1. Parse the `untrusted_url`.
2. If it is a relative path starting with a single `/` (e.g., `/dashboard`), it is valid. (Note: protocol-relative URLs starting with `//` are INVALID).
3. If it is an absolute URL:
   - The scheme MUST be exactly `https`.
   - The hostname MUST exactly match the `allowed_base_domain`, OR be a valid subdomain (e.g., `app.example.com` is valid for `example.com`, but `notexample.com` is INVALID).
4. The path component of the URL must NOT contain `../` or `%2e%2e/` (case-insensitive).
5. If the URL is valid, output exactly: `SAFE: <original_untrusted_url>` to standard output (no trailing newline is strictly required, but standard is fine).
6. If the URL violates any rule, output exactly: `INVALID` to standard output.
7. Any parsing error should result in `INVALID`.

Ensure your script has executable permissions (`chmod +x /home/user/validate_redirect`). 

An automated fuzzer will run your script with thousands of randomly generated URLs and base domains to ensure it perfectly matches our reference security oracle.