You are a DevSecOps engineer implementing "policy as code" for a custom file upload handler. Your system receives text files and encrypted log files in the `/home/user/uploads` directory.

Recent audits show the upload handler is susceptible to Path Traversal and Stored XSS because it fails to sanitize inputs before processing.

Your task is to write a Python script at `/home/user/scan_uploads.py` that performs the following automated policy enforcement:

1. **Scan Directory:** Iterate through all files in `/home/user/uploads`.
2. **Decrypt Encrypted Logs:** Files with a `.enc` extension are encrypted with a single-byte XOR cipher. You must brute-force the decryption key (0x00 to 0xFF). A correctly decrypted file will contain printable ASCII text, and you should scan its plaintext content.
3. **Vulnerability Analysis:** Check the plaintext content of all files (both standard text files and decrypted `.enc` files) for the following exact malicious signatures:
    - Path Traversal: `../`
    - XSS: `<script` or `onerror=`
4. **Access Control:** Modify the file permissions in the `/home/user/uploads` directory based on your findings:
    - If a file contains any malicious signatures, set its permissions to `0000` (no access).
    - If a file is completely safe, set its permissions to `0644` (read/write for owner, read for others).
5. **Reporting:** Generate a JSON report at `/home/user/report.json` mapping the original file names to their status (`"safe"` or `"malicious"`).

Example format for `/home/user/report.json`:
```json
{
  "log1.txt": "safe",
  "payload.txt": "malicious",
  "secret.enc": "malicious"
}
```

Run your script to process the files and generate the report.