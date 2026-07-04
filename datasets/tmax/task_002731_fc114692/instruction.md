You are acting as a penetration tester analyzing a custom web backend written in Rust. 

You have been provided with a file at `/home/user/upload_handler.rs`. This file contains the source code for a web server's file upload handling and authentication module.

Your task is to analyze the source code and identify several security vulnerabilities:
1. **Authentication Bypass**: The token generation is deterministic and uses a hardcoded salt. Identify the salt and compute the valid token for the username `admin`.
2. **Path Traversal**: The file upload handler blindly constructs file paths. Determine the exact `filename` payload required to overwrite the file at `/var/www/html/index.html` given the base upload directory specified in the code.
3. **Missing Security Headers**: The HTML response is missing a crucial security header used to prevent Cross-Site Scripting (XSS) by restricting the sources of executable scripts. Identify the standard HTTP header name for this (e.g., X-Frame-Options, Strict-Transport-Security, etc. - you must find the specific one for script sources).

Once you have identified these flaws, write a Rust program at `/home/user/exploit_gen.rs`. Your Rust program must calculate the necessary cryptographic hashes and output the results to a JSON file at `/home/user/report.json`.

The `/home/user/report.json` must have the following exact structure:
```json
{
  "admin_token": "<the computed valid token for 'admin'>",
  "path_traversal_payload": "<the exact filename payload>",
  "missing_header": "<The-Name-Of-The-Missing-Header>",
  "token_sha256": "<the SHA-256 hash of the admin_token>"
}
```

Constraints:
- You must use Rust to write the script that generates the JSON file. You may use `std::process::Command` to invoke external hashing utilities like `md5sum` or `sha256sum`, or you can use external crates if you set up a Cargo project in `/home/user/exploit_workspace`.
- Ensure the JSON file is properly formatted and saved exactly at `/home/user/report.json`.