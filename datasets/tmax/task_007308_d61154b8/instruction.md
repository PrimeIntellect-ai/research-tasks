You are an incident responder investigating a potential supply chain attack on a web application's static files. An attacker may have modified HTML files to inject malicious inline scripts. The site uses a strict Content Security Policy (CSP) with allowed script hashes, but you suspect some files bypass this policy and have had their permissions altered to maintain persistence.

Your task is to write a Go program at `/home/user/check_csp.go` that automates this investigation. 

You have the following resources:
1. A directory containing the web files: `/home/user/webroot/`
2. A file containing the allowed CSP script hashes (one per line): `/home/user/valid_csp.txt`

Your Go program must do the following:
1. Recursively scan the `/home/user/webroot/` directory for any files with an `.html` extension.
2. For each `.html` file, find all inline script tags. For simplicity, assume the tags are exactly formatted as `<script>` (start) and `</script>` (end), all on a single line or spanning multiple lines. Extract the exact string content *between* `<script>` and `</script>` (including any leading/trailing whitespaces or newlines).
3. Compute the SHA-256 hash of each extracted script's content, and base64-encode the raw binary hash. Format it as `sha256-<base64_string>` (this is how CSP hashes are formatted).
4. Check if the computed hash exists in `/home/user/valid_csp.txt`.
5. If an HTML file contains *any* unauthorized script (a script whose hash is not in the valid list), record it as compromised.
6. For each compromised file, read its UNIX file permissions (e.g., 0644, 0666, 0777).
7. Output the results to a JSON file at `/home/user/report.json`.

The JSON output must be an array of objects, sorted alphabetically by the `file` path, with the following format:
```json
[
  {
    "file": "/home/user/webroot/sub/malicious.html",
    "unauthorized_hashes": ["sha256-..."],
    "permissions": "0666"
  }
]
```
Note: `unauthorized_hashes` should be an array of strings containing all unauthorized hashes found in that specific file, sorted alphabetically. The `permissions` string should be a 4-digit octal representation of the file's permission bits (e.g., "0644").

Run your Go program and ensure `/home/user/report.json` is successfully created with the correct findings.