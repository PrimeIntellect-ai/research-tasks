You are an application security engineer tasked with rotating credentials and securing a legacy application component. The legacy application resides in `/home/user/app_legacy`.

Your objectives are:
1. **ELF Analysis & File Integrity**: 
   - Analyze the compiled binary `/home/user/app_legacy/worker_bin` to extract the hardcoded legacy database password and the legacy database IP address. The strings are formatted as `DB_PASS=<password>` and `DB_IP=<ip>`.
   - Verify the integrity of `worker_bin` by comparing its SHA256 hash against the hash provided in `/home/user/app_legacy/checksums.txt`.

2. **Code Auditing & Credential Rotation**:
   - Audit the Python script `/home/user/app_legacy/service.py`. Identify the standard MITRE CWE identifier for the vulnerability related to "Use of Hard-coded Credentials".
   - Modify `/home/user/app_legacy/service.py` to remove the hardcoded password. Make it read the password from the file `/home/user/secrets/db_pass.txt` instead.
   - Create the directory `/home/user/secrets` and the file `/home/user/secrets/db_pass.txt` containing the new password: `SecureRotatedPass2024!`.

3. **Network Policy Configuration**:
   - Create an application-level firewall policy file at `/home/user/app_legacy/net_policy.json`. It must be valid JSON with the following structure, utilizing the database IP address you extracted from the binary:
     ```json
     {
       "allowed_ips": ["<extracted_ip>"],
       "action": "allow"
     }
     ```

4. **Reporting**:
   - Generate a JSON report at `/home/user/rotation_report.json` with the following exact keys and your findings:
     ```json
     {
       "old_password": "<extracted_old_password>",
       "worker_bin_valid": <true or false boolean based on hash check>,
       "python_cwe": "<CWE-ID>",
       "db_ip": "<extracted_ip>"
     }
     ```
     (For `python_cwe`, format it exactly as `CWE-XXX` where XXX is the number).

Make sure all paths, file names, and JSON keys are exactly as specified.