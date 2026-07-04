You are a compliance analyst tasked with generating an audit trail for a web server. The server recently suffered a security breach, and we suspect multiple attack vectors were used, including path traversal, SQL injection (SQLi), and Cross-Site Scripting (XSS). Additionally, some files uploaded to the server may have been tampered with.

Your objective is to write a Python script at `/home/user/audit.py` that processes the web server logs, identifies malicious activity, verifies the integrity of uploaded files, quarantines tampered files, and generates a structured audit report.

**Inputs provided to you:**
1. **Server Logs**: `/home/user/server_logs.json`
   A JSON array of log entries. Each entry is a dictionary containing:
   - `ip`: Source IP address (string)
   - `method`: HTTP method (string)
   - `path`: Request path and query string (string)
   - `headers`: A dictionary of HTTP headers, including `User-Agent` and `Cookie` (keys are case-sensitive as provided in the JSON)
   - `uploaded_file_id`: The filename of the uploaded file, if any (string or null)

2. **Uploaded Files**: `/home/user/uploads/`
   A directory containing the physical files corresponding to `uploaded_file_id`.

3. **Known Good Hashes**: `/home/user/hashes.txt`
   A text file containing the expected SHA256 checksums of the uploaded files.
   Format: `<sha256_hash>  <uploaded_file_id>` (two spaces between hash and filename).

**Your script must perform the following actions:**

**1. Threat Detection (Log Analysis):**
Analyze each log entry for malicious payloads in the `path`, `User-Agent` header, or `Cookie` header. An IP should be flagged as malicious if any of its requests contain the following exact substring matches (case-sensitive):
- **Path Traversal**: `../` or `%2e%2e%2f` (checked in `path` only)
- **SQLi**: `' OR ` or `UNION SELECT` (checked in `path` or `Cookie`)
- **XSS**: `<script>` (checked in `path` or `User-Agent`)

**2. File Integrity Verification & Access Control:**
For any log entry that contains an `uploaded_file_id` (not null):
- Compute the SHA256 hash of the file located at `/home/user/uploads/<uploaded_file_id>`.
- Compare the computed hash against the expected hash in `/home/user/hashes.txt`.
- If the file's hash **does not match** the expected hash, you must quarantine the file by changing its file permissions to `0400` (read-only for the owner, no permissions for group/others).

**3. Generate the Audit Trail:**
Output a JSON report to `/home/user/audit_trail.json` with the exact following structure:
```json
{
  "malicious_ips": ["list", "of", "ips"],
  "quarantined_files": ["list", "of", "file_ids"]
}
```
- `malicious_ips`: A deduplicated, alphabetically sorted list of IP addresses that sent at least one malicious request.
- `quarantined_files`: A deduplicated, alphabetically sorted list of `uploaded_file_id`s that failed the integrity check.

**Execution:**
Once your script is written, run it to process the data, modify the necessary file permissions, and generate `/home/user/audit_trail.json`. The automated test will verify the contents of your output JSON and the file permissions in the uploads directory.