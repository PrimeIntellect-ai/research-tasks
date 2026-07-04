You are a network security engineer investigating a custom login server. Recently, suspicious traffic has been hitting the server, and there are reports of an open redirect vulnerability and sensitive data leakage. 

You have been given two files in your home directory (`/home/user/`):
1. `server_bin`: The compiled binary of the legacy login server.
2. `traffic.jsonl`: A log file containing intercepted HTTP requests and responses in JSON Lines format.

Your task is to analyze the binary, write a Go program to process the traffic logs, and output a sanitized and analyzed report.

Step 1: Reverse Engineering
Analyze `/home/user/server_bin`. The original developers hardcoded two important configuration strings in this binary:
- A trusted domain used for internal redirects (look for a string starting with `TRUSTED_DOMAIN=`).
- The name of a highly privileged session cookie (look for a string starting with `SECRET_COOKIE_NAME=`).

Step 2: Data Processing and Analysis
Write a Go program at `/home/user/analyze.go` that reads `/home/user/traffic.jsonl` line by line. Each line is a JSON object with the following structure:
```json
{
  "request_id": "12345",
  "method": "GET",
  "url": "/login?redirect=http://example.com/dashboard",
  "headers": {
    "Cookie": "session=abc; other_cookie=def",
    "User-Agent": "Mozilla/5.0"
  }
}
```

Your Go program must process each entry and output a new JSON Lines file to `/home/user/processed_traffic.jsonl` with the following transformations:
1. **Sensitive Data Redaction**: Inspect the `Cookie` header. If the privileged session cookie (identified in Step 1) is present, replace its value with `[REDACTED]`. Maintain the format of the other cookies.
2. **Open Redirect Identification**: Parse the `url`. If there is a `redirect` query parameter, check if its host matches the `TRUSTED_DOMAIN` found in Step 1. If it contains a domain that does NOT match the trusted domain exactly, add a new boolean field to the JSON object: `"open_redirect_attempt": true`. If it matches, or if there is no redirect parameter, set it to `false`.
3. **CSP Enforcement**: Add a new key `"injected_csp"` to the JSON object. Its value must be exactly `"default-src 'self'; frame-ancestors 'none'; connect-src https://<TRUSTED_DOMAIN>"` (replace `<TRUSTED_DOMAIN>` with the actual domain found in Step 1).

Requirements:
- Ensure the output file `/home/user/processed_traffic.jsonl` is valid JSONL.
- Do not modify the `request_id`, `method`, or unmodified headers.
- Build and execute your Go program to generate the final output.