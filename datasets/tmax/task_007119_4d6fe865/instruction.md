You are acting as a compliance analyst generating an automated audit trail for a new internal web service deployment.

A staging deployment artifact is located at `/home/user/deploy_artifact/`. You need to write a Python script at `/home/user/audit_trail.py` that performs a security audit on this directory and generates a strict JSON report at `/home/user/audit_report.json`.

Your script must perform the following checks on the files inside `/home/user/deploy_artifact/`:

1. **File Integrity Verification**: 
   Read the `manifest.txt` file (format: `SHA256_HASH FILENAME` per line). Calculate the SHA256 hash of each file listed and identify any files where the calculated hash does not match the manifest.
   
2. **Certificate Chain Validation**:
   The directory contains `server.crt` and `ca.crt` (both in PEM format). Programmatically verify if `server.crt` was validly issued/signed by `ca.crt`. (You may use external commands via `subprocess` like `openssl verify` or a Python library).

3. **Automated Vulnerability Scanning**:
   Scan all `.py` files in the directory for simple command injection sinks. Specifically, flag any file that contains the exact substring `os.popen(`.

4. **Privilege Escalation Auditing**:
   Check the POSIX file permissions of all files in the directory. Identify any file that is "world-writable" (i.e., others have write permissions), as this could allow local privilege escalation or configuration tampering.

**Output Format:**
Your script must output a JSON file at `/home/user/audit_report.json` with exactly the following structure:
```json
{
  "integrity_failures": ["list of filenames (e.g. 'app.py') that failed the hash check"],
  "certificate_valid": true_or_false,
  "vulnerable_files": ["list of .py filenames containing the prohibited substring"],
  "world_writable_files": ["list of filenames that are world-writable"]
}
```

Constraints:
* Do not use absolute paths in the lists inside the JSON; use only the base filenames (e.g., `app.py`, `config.yaml`).
* Your script should be fully self-contained and runnable via `python3 /home/user/audit_trail.py`.