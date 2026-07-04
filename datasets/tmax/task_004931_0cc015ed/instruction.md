You are tasked with troubleshooting and fixing a broken log analysis and reverse proxy setup. 

The system currently suffers from two main issues:
1. An Nginx configuration is misconfigured, causing 502 Bad Gateway errors when attempting to reach the backend service.
2. The backend service, a custom log sanitizer written in Rust, fails to compile and crashes on standard inputs.

Perform the following tasks:

**Phase 1: Backup and Nginx Configuration**
1. Ensure you have a backup of the current Nginx configuration. Create a backup of `/home/user/nginx_setup/nginx.conf` and save it precisely to `/home/user/backup/nginx.conf.bak`. Create the backup directory if it does not exist.
2. The Nginx configuration at `/home/user/nginx_setup/nginx.conf` has a misconfigured `proxy_pass` directive pointing to `127.0.0.1:9999`. Use text processing tools (like `sed` or `awk`) to change this upstream port to `8080`.

**Phase 2: Fix the Vendored Rust Package**
1. We have a vendored third-party Rust package called `log-sanitizer` located at `/app/log-sanitizer`. 
2. This tool is designed to read log lines from `stdin` and print sanitized logs to `stdout`. It should drop any log line that contains malicious signatures, specifically: `../` (path traversal), `UNION SELECT` (SQLi), or `<script>` (XSS).
3. Currently, the package is broken. It fails to compile due to missing dependencies, and its source code contains a deliberate bug that causes it to panic on valid log entries.
4. Fix the `Cargo.toml` and `src/main.rs` so that the tool successfully compiles.
5. Implement the filtering logic. The tool must output ONLY the clean lines and completely drop the lines containing the malicious signatures.

**Phase 3: Verification Preparation**
1. Once fixed, compile the Rust project in release mode.
2. Copy the resulting executable to `/home/user/bin/log-sanitizer`. (Create the directory if needed).
3. Ensure your tool correctly handles the data in `/app/corpora/clean/` (where all lines must be preserved) and `/app/corpora/evil/` (where all lines containing the signatures must be dropped).