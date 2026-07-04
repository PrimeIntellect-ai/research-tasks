You are acting as a security auditor reviewing server logs for a web application. You have been provided with an access log file located at `/home/user/auth_logs.txt`. The application has a known open redirect vulnerability in its login flow, specifically within the `redirect_to` parameter of the `/login` endpoint.

Your task consists of the following four steps:

1. **Sensitive Data Redaction**: The log file contains active session tokens which must not be exposed in your audit report. Write a Python script to read `/home/user/auth_logs.txt` and replace all occurrences of the session token values with the exact string `[REDACTED]`. The tokens are found at the end of the log lines in the format `session_id=...` (where the ID is an alphanumeric string). Save the cleaned log to `/home/user/redacted_logs.txt`. Keep the `session_id=` part intact, so it becomes `session_id=[REDACTED]`.

2. **Intrusion Detection (Pattern Matching)**: Analyze the logs to find all open redirect attempts. An open redirect attempt is any request to `/login` where the `redirect_to` parameter contains an absolute external URL (i.e., starting with `http://` or `https://`). Extract only these external target URLs. Sort them alphabetically and save them to `/home/user/redirect_targets.txt`, with one URL per line.

3. **Checksum Verification**: To ensure the integrity of the redacted log file for the compliance team, calculate its SHA256 checksum. Save the output to `/home/user/log_checksum.txt` in the standard format produced by the `sha256sum` command (e.g., `<hash>  /home/user/redacted_logs.txt`).

4. **Exploit Crafting**: Create a Proof of Concept (PoC) URL that demonstrates the vulnerability. The local vulnerable application is hosted at `http://127.0.0.1:5000`. Craft a complete URL that exploits the `/login` endpoint's open redirect vulnerability to redirect a victim to `http://attacker.com/steal`. Save ONLY this exact PoC URL string to `/home/user/poc.txt`.

Ensure all files are created exactly at the specified paths in `/home/user/` and follow the requested formats.