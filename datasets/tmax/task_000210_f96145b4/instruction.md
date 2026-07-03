You have been assigned to perform a security audit on a local file upload handler script. 

The target system has the following setup:
- The upload handler script is located at `/home/user/upload_handler.py`. It simulates a backend endpoint that accepts a token, a filename, and base64-encoded file content as command-line arguments.
- The handler is intended to only upload files into `/home/user/target_dir/`.
- There is a highly sensitive directory at `/home/user/protected/` which you must not normally be able to write to.
- The HMAC-SHA256 secret key used for token generation is stored in `/home/user/secret.key`.

Your objective is to:
1. Audit `/home/user/upload_handler.py` to understand its token validation and identify the vulnerability in how it handles file paths.
2. Determine the standard CWE ID (e.g., "CWE-XXX") for the identified path traversal vulnerability.
3. Write a Python exploit script at `/home/user/exploit.py` that:
   - Reads the secret key and dynamically generates a valid authentication token for the payload string `user=auditor`.
   - Utilizes payload encoding to bypass the naive path traversal filter in the handler.
   - Executes `/home/user/upload_handler.py` with the generated token, the crafted filename payload, and base64-encoded content to successfully write a file named `pwned.txt` containing the exact string `SUCCESS` inside the `/home/user/protected/` directory.
4. Execute your `exploit.py` script to ensure it works.
5. Create a JSON log file at `/home/user/audit_result.json` containing your findings with the following exact structure:
```json
{
  "cwe_id": "CWE-XX",
  "token": "<the_generated_valid_token_string>"
}
```

Constraints:
- Do not modify `/home/user/upload_handler.py` or `/home/user/secret.key`.
- The `audit_result.json` file must contain the exact CWE ID standard for "Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')" and the exact token string your script generated and used.