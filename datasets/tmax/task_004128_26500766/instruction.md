You are a DevSecOps engineer tasked with enforcing policy as code. We have discovered that our web server's login flow might be under attack. We've exported a sample of recent access logs to `/home/user/logs.json`.

Your task is to write a Rust CLI tool that parses these logs, detects specific vulnerabilities based on payloads and encodings, and outputs a structured findings report.

1. Create a new Rust project at `/home/user/scanner`.
2. The tool must read `/home/user/logs.json`, which contains a JSON array of log entries. Each entry has the following structure:
   ```json
   {
     "id": "string",
     "url": "string (e.g., '/login?redirect=...')",
     "headers": {
       "Authorization": "string (e.g., 'Basic dXNlcjpwYXNz')"
     }
   }
   ```
3. Analyze each log entry for the following security flags:
   - **`open_redirect`**: The `url` contains a query parameter named `redirect`. After fully URL-decoding its value, if the value starts with `http://` or `https://` but does NOT start with `http://example.com` or `https://example.com`, flag it.
   - **`xss`**: The `url` contains a `redirect` parameter. After fully URL-decoding its value, if the decoded string contains the substring `<script` (case-insensitive) or `javascript:` (case-insensitive), flag it.
   - **`privesc`**: The `Authorization` header (if present) starts with `Basic `. The remainder of the string is a Base64-encoded payload. Decode this Base64 payload. If the decoded UTF-8 string contains the exact substring `role=admin`, flag it as a privilege escalation attempt.

4. Generate a JSON report at `/home/user/findings.json`. The output must be a JSON array of objects, containing only the logs that triggered at least one flag.
   - Each object must have an `"id"` (string) and `"flags"` (array of strings).
   - The `"flags"` array must be sorted alphabetically (e.g., `["open_redirect", "privesc"]`).
   - The outer JSON array must be sorted alphabetically by the `"id"` field.
   
Example output format for `/home/user/findings.json`:
```json
[
  {
    "id": "log1",
    "flags": ["open_redirect"]
  },
  {
    "id": "log2",
    "flags": ["privesc", "xss"]
  }
]
```

You are free to use any Rust crates (e.g., `serde_json`, `url`, `base64`, `percent-encoding`) by adding them to your `Cargo.toml`. When finished, compile and run your tool so that `/home/user/findings.json` is successfully created.