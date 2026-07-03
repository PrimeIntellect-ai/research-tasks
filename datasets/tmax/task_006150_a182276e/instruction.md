You are acting as a compliance analyst for a web application. We suspect an issue with our file upload handler and its security policies. You need to investigate the server logs, inspect HTTP headers, verify file integrity, and generate an audit trail.

You have been provided with an audit directory at `/home/user/audit_data`. 
Inside, there is a log file named `server.log` containing JSON Lines (JSONL). Each line represents an HTTP request processed by the server. 
There are also files on the disk that were created by these requests.

Your task is to analyze the log and the filesystem to generate a security audit report based on the following criteria:

1. **CSP Enforcement Check**: Analyze the `resp_headers` for all requests to the `/upload` endpoint. Flag any request that does *not* contain the exact header: `"Content-Security-Policy": "default-src 'self'"` (case-sensitive on the key and value).
2. **Path Traversal Identification**: The application intends to save all uploads to `/home/user/audit_data/uploads/`. Inspect the `file_saved_path` field in the logs. Flag any request where the saved file path is located *outside* the intended `uploads` directory (e.g., a file written directly to `/home/user/audit_data/` or elsewhere). 
3. **Session Correlation**: For every request flagged by either step 1 (CSP failure) or step 2 (Path Traversal), extract the session ID from the `Cookie` header (format: `session_id=<value>;` or just `session_id=<value>`).
4. **File Integrity Verification**: For every file that resulted from a **Path Traversal**, locate the actual file on disk and compute its SHA-256 hash.

Generate an audit report at `/home/user/audit_report.json` matching this exact JSON structure:
```json
{
  "flagged_requests": ["req_id1", "req_id2"],
  "compromised_sessions": ["session_value1", "session_value2"],
  "traversed_files_hashes": {
    "/absolute/path/to/escaped/file": "sha256_hex_digest"
  }
}
```
*Note: Sort the arrays alphabetically in the output JSON. The `traversed_files_hashes` object should contain the absolute paths as keys and their corresponding SHA-256 hex digests as values.*