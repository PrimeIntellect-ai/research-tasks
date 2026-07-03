You are a network engineer troubleshooting connectivity and security issues for an internal server. Recently, users have reported being unable to log in via SSH, while the server has also been subjected to a barrage of strange authentication anomalies. You need to extract the new port configuration from a provided diagram, update your environment, generate a firewall configuration, and write a Python script to detect the specific SSH misconfiguration causing silent key rejections.

Here are your tasks:

1. **Extract Configuration from Image**:
   There is an image at `/app/fw_spec.png` containing the new port assignments. Use OCR (e.g., `tesseract`) to extract the text. You will find variables for `SSH_PORT` and `EMAIL_PORT`.

2. **Environment Setup**:
   Append export statements for `SSH_PORT` and `EMAIL_PORT` (using the exact values extracted from the image) to `/home/user/.bashrc`.

3. **Firewall Rules Generation**:
   Write a Python script `/home/user/fw_generator.py` that reads `SSH_PORT` and `EMAIL_PORT` from the environment and creates a file `/home/user/fw_rules.txt` with the following exact lines:
   ```
   iptables -A INPUT -p tcp --dport <SSH_PORT> -j ACCEPT
   iptables -A INPUT -p tcp --dport <EMAIL_PORT> -j ACCEPT
   ```

4. **Log Classifier (Adversarial Corpus)**:
   We need to filter out logs where SSH silently rejects key-based logins (often due to strict permissions issues like "bad ownership or modes"). 
   You are provided with two directories containing sample log snippets:
   - `/app/corpora/clean/`: Contains normal SSH logs (successful logins, or standard password failures).
   - `/app/corpora/evil/`: Contains SSH logs indicating silent key-based login rejections due to bad file/directory permissions.

   Write a Python script at `/home/user/detector.py` that takes a single file path as a command-line argument.
   - If the log file contains the "evil" pattern (silent key rejection due to permissions), the script MUST print exactly `EVIL` to standard output.
   - If the log file is "clean", it MUST print exactly `CLEAN` to standard output.
   Your script will be tested against a holdout dataset of clean and evil logs. It must achieve 100% accuracy on both.

5. **Log Rotation Setup**:
   Create a log rotation configuration file at `/home/user/logrotate.conf` to rotate the email server logs located at `/var/log/mail.log`. The configuration must specify:
   - Daily rotation
   - Keep 7 days of logs
   - Compress the old logs
   - Missing logs should not generate an error

Complete all steps and ensure `/home/user/detector.py` is fully functional.