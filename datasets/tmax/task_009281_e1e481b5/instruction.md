You are acting as a compliance analyst generating an automated audit trail for a web server. We have discovered an open redirect vulnerability in the server's login flow that attackers are using to craft malicious links, potentially leading to privilege escalation if the redirect targets sensitive administrative endpoints on external, attacker-controlled infrastructure.

Your task is to create a Rust program that analyzes the server logs, identifies exploitation attempts, decodes the payloads, evaluates the presence of specific Content Security Policy (CSP) protections, and produces a structured JSON audit report.

Create a Rust project in `/home/user/audit_tool` (e.g., using `cargo new`).
Write the logic to perform the following:

1. **Parse Access Logs:**
   Read the file `/home/user/auth_logs.txt`. Each line follows this format:
   `[TIMESTAMP] [IP] [METHOD] [PATH] [PROTOCOL]`
   For example: `2023-10-01T10:05:00Z 10.0.0.5 GET /login?return_url=https%3A%2F%2Fevil.com%2Fadmin%2Fescalate%3Fuser%3Dtest HTTP/1.1`

2. **Pattern Matching & Payload Decoding:**
   For each log line, check if the `PATH` contains the parameter `return_url=`. 
   If it does, extract the value of this parameter and perform URL-decoding to get the plaintext URL. 

3. **Intrusion Detection & Privilege Escalation Auditing:**
   Analyze the decoded URL to determine if it is a malicious privilege escalation attempt. Flag the request ONLY if ALL the following conditions are met:
   - The decoded URL starts with `http://` or `https://`.
   - The domain in the decoded URL is NOT `internal.corp` (e.g., `http://internal.corp/home` is safe).
   - The decoded URL's path contains either `/admin/` or `/su/` anywhere within it.

4. **Content Security Policy Enforcement Verification:**
   Read the file `/home/user/csp.txt`, which contains the server's HTTP CSP header.
   Check if the header string contains the exact sub-string `'strict-dynamic'`.

5. **Generate Audit Trail:**
   Output the findings to a JSON file at `/home/user/audit_report.json` with the exact following structure:
   ```json
   {
     "csp_is_strict": true,  // boolean, true if 'strict-dynamic' is present in csp.txt
     "escalation_attempts": [
       {
         "ip": "10.0.0.5",
         "decoded_url": "https://evil.com/admin/escalate?user=test"
       }
     ]
   }
   ```
   (The `escalation_attempts` array must preserve the order of appearance in the log).

You may use third-party crates like `serde`, `serde_json`, and `urlencoding` by adding them to your `Cargo.toml`. Compile and run your program to generate the required `/home/user/audit_report.json` file.