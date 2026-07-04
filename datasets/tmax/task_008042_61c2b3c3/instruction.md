You are acting as a digital forensics analyst investigating a compromised Linux host. We have collected artifacts from the machine, but they contain both normal user traffic and malicious activity.

We discovered that a rogue background process was executed with a sensitive authentication token leaked directly in its command-line arguments (which was visible in `/proc/[PID]/cmdline`). 

Your task is to build a custom Rust tool that extracts this leaked token, identifies unauthorized HTTP requests in our captured logs that used this token, and redacts the sensitive stolen data from those logs so they can be safely shared with our external auditing firm.

**Evidence Provided (Assume these exist on the system):**
1. `/home/user/evidence/proc_cmdline.b64`: A base64 encoded snapshot of the compromised process's command line (since the original contained null bytes). 
2. `/home/user/evidence/http_logs.jsonl`: A JSON Lines file containing intercepted HTTP traffic. Each line is a JSON object representing an HTTP request with the following structure:
   `{"timestamp": "...", "method": "...", "url": "...", "headers": {"Header1": "Val1", ...}, "cookies": "cookie1=val1; cookie2=val2", "body": "..."}`

**Your Objectives:**
1. **Initialize a Rust project:** Create a new Rust project named `forensics_cleaner` in `/home/user/forensics_cleaner`. You may use standard crates like `serde` and `serde_json`.
2. **Extract the token:** Your Rust program must read `/home/user/evidence/proc_cmdline.b64`, decode the base64, and parse the null-byte (`\x00`) separated command line arguments. Find the argument that starts with `--master-auth-token=` and extract the token value.
3. **Inspect HTTP Logs:** Read `/home/user/evidence/http_logs.jsonl` line by line.
4. **Identify Malicious Requests:** A request is considered malicious if:
   - The `headers` object contains an `Authorization` header with the exact value: `Bearer <extracted_token>`
   - OR the `cookies` string contains `session=<extracted_token>` (it might be part of a larger cookie string, e.g., `user=admin; session=token_value; theme=dark`).
5. **Redact Sensitive Data:** If a request is identified as malicious:
   - Redact the token from the `Authorization` header (if present) so it reads `Bearer [REDACTED]`.
   - Redact the token from the `cookies` string (if present) so that specific value is replaced, resulting in `session=[REDACTED]`.
   - Completely replace the contents of the `body` field with the exact string `[REDACTED]`.
6. **Pass-through Normal Requests:** Any request that does NOT use the extracted token must remain completely unmodified.
7. **Output:** Write the processed JSON Lines to `/home/user/evidence/cleaned_logs.jsonl`. Ensure the JSON structure and keys remain identical to the input.

Write, build, and run this Rust tool to produce the final `cleaned_logs.jsonl` file.