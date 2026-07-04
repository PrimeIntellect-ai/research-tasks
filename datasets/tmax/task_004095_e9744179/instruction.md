As a compliance analyst, you need to generate a cryptographic audit trail for a recent incident where a web server's file upload handler was susceptible to path traversal (CWE-22). 

You are provided with an access log at `/home/user/logs/upload.log` and the web server's mock filesystem starting at `/home/user/server_root/`. The expected, safe upload directory is `/home/user/server_root/uploads/`.

Your task is to write a Rust tool to parse the logs, detect vulnerabilities, verify file integrity, and generate a structured audit trail.

Instructions:
1. Initialize a new Rust project in `/home/user/audit_tool/`.
2. Write a Rust program that reads `/home/user/logs/upload.log`. The log format is:
   `<timestamp> <method> <path>?filename=<filename> <status>`
   Example: `2023-10-01T10:00:00Z POST /api/upload?filename=image.png 200`
3. Identify all successful (status `200`) `POST` requests to `/api/upload`.
4. Determine if the `filename` parameter contains a path traversal attempt that successfully escapes the intended `/home/user/server_root/uploads/` directory.
5. For each escaping file that actually exists on disk (resolving the traversal relative to `/home/user/server_root/uploads/`), compute its SHA-256 hash.
6. The Rust tool must output a JSON array to `/home/user/audit_report.json` containing the findings, ordered by the log timestamp.

The JSON array must contain objects with the following exact keys:
- `timestamp`: The exact timestamp string from the log.
- `provided_filename`: The raw filename parameter extracted from the log URL.
- `resolved_path`: The canonical, absolute path of the file on disk (e.g., `/home/user/server_root/etc/config.txt`).
- `sha256`: The computed SHA-256 hash of the file contents (lowercase hex string).
- `cwe`: The literal string `"CWE-22"`.

Only include entries for status `200` requests where the resolved path is strictly outside `/home/user/server_root/uploads/` and the file physically exists on disk.
Build and run your Rust tool to generate `/home/user/audit_report.json`.