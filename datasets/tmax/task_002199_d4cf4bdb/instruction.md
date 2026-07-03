You are a DevSecOps engineer tasked with analyzing and securing a legacy authentication CGI program written in C. 

The workspace is located at `/home/user/workspace`. 
Inside, you will find two files:
1. `login.c`: The purported source code of the authentication handler.
2. `login.cgi`: The currently deployed, compiled binary of the authentication handler.

We suspect the compiled binary `login.cgi` has been compromised with a backdoor not present in `login.c`, and that `login.c` itself contains security flaws (Policy-as-Code violations).

Your task has three parts: Reverse Engineering, Code Auditing, and Secure Remediation.

**Part 1: Reverse Engineering & Disassembly**
Analyze the `login.cgi` binary to find a hidden, hardcoded malicious URL that it redirects administrators to. 
Create a report file at `/home/user/workspace/report.txt`.
- On line 1 of `report.txt`, write the exact malicious URL you found in the binary.

**Part 2: Code Auditing (CWE Identification)**
Review `login.c`. It takes a `next` parameter from the `QUERY_STRING` environment variable and constructs an HTTP `Location` header to redirect the user. It currently trusts user input implicitly.
- Identify the exact CWE ID for this specific "open redirect / unvalidated redirect" vulnerability.
- On line 2 of `report.txt`, write the CWE ID in the format: `CWE-XXX` (e.g., CWE-123).

**Part 3: Secure Remediation & Sensitive Data Redaction**
The `login.c` program writes an audit trail to `/home/user/workspace/audit.log`, logging the `HTTP_COOKIE` environment variable. This leaks sensitive `SessionID` values.

Create a fixed version of the source code and save it as `/home/user/workspace/fixed_login.c`.
Make the following security fixes:
1. **Fix the Redirect:** Read the `next` value from `QUERY_STRING` (format: `next=...`). If the value does not start with exactly a single forward slash `/` (e.g., `/dashboard`), or if it starts with two forward slashes `//` (e.g., `//evil.com`), default the redirect to `/index.html`. Otherwise, use the provided `next` value. Output the HTTP `Location: <url>` header and a blank line.
2. **Redact Sensitive Logs:** When logging to `audit.log`, inspect the cookie string. If it contains `SessionID=<value>`, replace the value with `REDACTED` (so it becomes `SessionID=REDACTED`) before writing to the log. The redaction should stop at the next semicolon `;` or the end of the string. Other cookies must remain intact.

Compile your fixed source code into `/home/user/workspace/fixed_login.cgi` using standard `gcc`.

**Success Criteria:**
- `report.txt` must contain exactly two lines with the correct backdoor URL and CWE ID.
- `fixed_login.cgi` must securely handle Open Redirect attempts, printing the safe `/index.html` `Location` header.
- `fixed_login.cgi` must redact `SessionID` values written to `audit.log` but preserve the rest of the log structure.