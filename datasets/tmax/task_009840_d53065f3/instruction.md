You are assisting a network engineer inspecting suspicious traffic dumps. We have intercepted several raw payload files from an internal network tap, currently saved in `/home/user/intercepted/`. 

Your objective is to build an automated vulnerability scanner and policy enforcer in Go that processes these payloads, identifies known threats, extracts hidden credentials from zero-day exploits, and establishes safe file permissions.

Here are your instructions:

1. **Threat Intelligence Hashing & Firewall Policy:**
   Write a Go program at `/home/user/analyze.go`. This program must iterate through all files in `/home/user/intercepted/` and calculate their SHA256 checksums.
   Compare each hash against the known malicious signatures listed in `/home/user/threat_intel.db` (one SHA256 hash per line).
   Your Go program must generate a firewall policy log at `/home/user/firewall_policy.log`. For every file processed, append a line in the exact format:
   `[ACTION] /home/user/intercepted/filename`
   Where `[ACTION]` is `BLOCK` if the hash is in the threat intel database, and `ALLOW` if it is not.

2. **Exploit Payload Extraction:**
   One of the intercepted files will be marked as `ALLOW` because its hash is not yet in our database. However, traffic analysis indicates this is an obfuscated zero-day exploit payload dropping an unauthorized access token.
   We have reverse-engineered the obfuscation: the file is encrypted using a single-byte XOR cipher with the key `0x7A`.
   Extend your Go program to decrypt this specific allowed file in memory. The decrypted plaintext will contain a string formatted exactly as `SECRET_ACCESS_TOKEN=<token_value>`.
   Extract the `<token_value>`.

3. **Secure Storage and File Permissions:**
   Your program must save the extracted token value (just the value, no newlines or prefixes) to a new file at `/home/user/safe_token.txt`.
   Using Go or standard bash commands, strictly configure the file permissions of `/home/user/safe_token.txt` to be read-only by the owner (`0400`). Ensure no other users or groups have any access to this file.

4. **Reporting:**
   Finally, your Go program must produce a summary report at `/home/user/final_report.json` containing the findings. The JSON must exactly match this structure:
   ```json
   {
     "scanned_files": 3,
     "blocked_files": 2,
     "allowed_files": 1,
     "extracted_token": "<token_value>"
   }
   ```

Run your Go program to generate the required log, the secured token file, and the JSON report. You can use standard bash tools to aid you during development and debugging.