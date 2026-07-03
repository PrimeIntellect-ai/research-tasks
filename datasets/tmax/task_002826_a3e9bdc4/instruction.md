You are a Linux Systems Engineer responsible for hardening system configurations and establishing an automated auditing pipeline. You have been given a policy document screenshot and a sample set of configuration files to build a detection mechanism.

Your tasks are as follows:

1. **Extract Environment Policy**:
   There is an image at `/app/policy_screenshot.png` containing a snippet of the company's mandatory server policy. Use OCR (e.g., `tesseract`) to read the image and identify the required timezone (`TZ`) and locale (`LANG`). 
   Update `/home/user/.bashrc` to permanently export these exact `TZ` and `LANG` variables so they apply to all new shell sessions.

2. **Develop an Auditing Script**:
   We need a Python script to scan bash scripts, systemd unit files, and cron jobs for malicious backdoor techniques often left by attackers. 
   Write a Python script at `/home/user/config_auditor.py`.
   The script must take two positional arguments:
   `python3 /home/user/config_auditor.py <input_directory> <output_json>`
   
   It must read all files in `<input_directory>`, evaluate them, and output a JSON dictionary mapping the filename (just the basename) to either the string `"clean"` or `"evil"`.

   To help you build your detection logic, we have provided two training directories:
   - `/app/corpora/clean/`: Contains legitimate system configurations.
   - `/app/corpora/evil/`: Contains malicious configurations (e.g., reverse shells using `/dev/tcp`, `curl * | bash` downloaders, and unauthorized `/etc/shadow` modifications).
   
   Your script must correctly classify **100%** of the files in both training directories. The automated test will evaluate your script against a hidden dataset of similarly structured files.

3. **Scheduled Execution**:
   Set up a cron job for the `user` account that runs your script every 15 minutes. The cron job should execute:
   `python3 /home/user/config_auditor.py /opt/configs /home/user/audit_report.json`
   (Assume `/opt/configs` will be populated later; the cron job just needs to be registered).

Ensure your Python script relies only on standard libraries or libraries you install yourself.