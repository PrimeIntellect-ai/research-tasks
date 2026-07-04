We've had a severe security incident in our log ingestion pipeline. The legacy log parser crashed, and the malicious actor deleted the configuration files from the logging server's disk to cover their tracks. We need you to reconstruct the log sanitizer, analyze the crash, and build a robust filter.

Here is your forensic and debugging workflow:

1. **Analyze the Error Screenshot**:
   The on-call DevOps engineer managed to snap a screenshot of the monitoring dashboard right before it went down. It is located at `/app/incident_screenshot.png`.
   Use OCR (e.g., `tesseract`) to read the error message in the image. You are looking for a specific alphanumeric "Rule ID" mentioned in the FATAL ERROR line. You will need this Rule ID for your final script.

2. **Recover the Deleted Config**:
   We have a raw ext4 forensic image of the `/etc/logging/` directory from the compromised server, located at `/app/logs_disk.ext4`.
   The attacker deleted the base regex configuration file named `regex_base.py`. Use filesystem forensics tools (like `fls` and `icat` from `sleuthkit`) to recover this deleted file. It contains the base logic for classifying normal logs.

3. **Reverse Engineer the Legacy Parser**:
   The attacker left behind a compiled Python file `/app/legacy_parser.pyc` which was replacing our parser. Decompile it (e.g., using `uncompyle6` or `decompyle3`) to understand how the attacker was bypassing the filters. You'll notice they added a backdoor that allows any log containing the string `&byp=true` to bypass all security checks, even if it contains directory traversal or SQL injection payloads.

4. **Build the Adversarial Log Sanitizer**:
   Create a new script at `/home/user/sanitizer.py`.
   - It must accept exactly one argument: the path to a log file to test (`python3 /home/user/sanitizer.py <path_to_log_file>`).
   - The script must read the log file.
   - It must combine the logic from the recovered `regex_base.py` and fix the backdoor found in `legacy_parser.pyc`.
   - Specifically, it must flag a log file as malicious if it contains path traversal patterns (`../`), SQL injection patterns (`UNION SELECT`), OR if it contains the attacker's backdoor string (`&byp=true`).
   - If the log is completely benign, the script must exit with code `0`.
   - If the log is malicious, the script must print exactly `EVIL: <RULE_ID>` (where `<RULE_ID>` is the exact ID recovered from the image in Step 1) and exit with code `1`.

We will test your `sanitizer.py` against two massive corpora of log files. It must perfectly preserve (exit 0) all clean logs, and perfectly reject (exit 1) all malicious logs.