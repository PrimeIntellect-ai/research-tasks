You are acting as a security auditor for a legacy video-processing and file-upload system. You need to investigate recent attacks and build a robust filter to prevent future vulnerabilities.

There are two main objectives:

**Objective 1: Video Log Forensics**
We lost our text logs for the upload server, but we have a screen recording of the log tail session. 
Analyze the video located at `/app/upload_logs.mp4` (you can use `ffmpeg` to extract frames). The video shows HTTP POST requests to an upload endpoint. 
Identify all unique IP addresses that attempted a path traversal attack (any request containing `../` in the URL).
Write these unique IP addresses, one per line, to `/home/user/blocked_ips.txt`.

**Objective 2: Upload Sanitizer (Adversarial Corpus)**
The developers need a pre-hook script to validate incoming file upload requests. The requests are saved as JSON files before processing.
Create a Python script at `/home/user/upload_filter.py` that takes a single command-line argument: the path to a JSON file.

The JSON file has the following format:
```json
{
  "target_path": "uploads/user1/profile.jpg",
  "client_cert_pem": "-----BEGIN CERTIFICATE-----...",
  "intermediate_cert_pem": "-----BEGIN CERTIFICATE-----..."
}
```

Your script must determine if the upload is **safe** (exit with code `0`) or **malicious** (exit with code `1`).

An upload is **malicious** (and must be rejected) if ANY of the following are true:
1. **Path Traversal / Insecure Path**: The `target_path` contains `../`, `..\\`, resolves to a directory outside of the base `uploads/` directory, or is an absolute path.
2. **Invalid Certificate Chain**: The `client_cert_pem` is not validly signed by `intermediate_cert_pem`, OR the `intermediate_cert_pem` is not validly signed by our Root CA located at `/app/root_ca.pem`. (You may use standard Python libraries like `cryptography` or `OpenSSL` to verify this).
3. **Invalid Extension**: The `target_path` ends with dangerous extensions like `.sh`, `.py`, `.exe`, or `.php`.

An upload is **safe** if the path is safely contained within `uploads/`, has a safe extension, and the certificate chain cryptographically validates up to `/app/root_ca.pem`.

Your script will be tested against a hidden corpus of clean and evil JSON requests. 
Make sure your script writes nothing to stdout/stderr if successful, and exclusively uses the exit code for classification.