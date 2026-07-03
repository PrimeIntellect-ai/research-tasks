You are acting as a network engineer troubleshooting connectivity and security in our infrastructure. We have an in-house Python SSH auth log analysis service that is supposed to monitor connections and identify malicious or misconfigured SSH login attempts (e.g., deprecated key types, brute-force indicators, or silent key rejections). However, the service is currently failing, and we need you to fix the underlying library, write the classification script, and deploy it as a continuously running user-service.

Here are your tasks:

1. **Fix the Vendored Library**:
   We vendor a custom Python library called `ssh_log_parser` located at `/app/ssh_log_parser/`. A recent commit broke the SSH key type parsing, causing it to silently reject or misclassify modern ed25519 keys as "invalid", while also missing certain malformed legacy DSA keys.
   Investigate the `parser.py` file in this directory and fix the regex or parsing logic so that it correctly identifies valid SSH auth patterns. Do not modify the test files in the directory; only fix the library code.

2. **Develop the Classifier**:
   Using the fixed `ssh_log_parser` library, write a Python script at `/home/user/ssh_monitor.py`. This script must act as a CLI filter for SSH logs.
   - It should accept a directory path as an argument.
   - It must iterate over all `.log` files in that directory.
   - For each file, if the log represents a clean, secure, and successful authentication, the script should print `CLEAN: <filename>` to standard output.
   - If the log contains malicious patterns, deprecated algorithms (e.g., ssh-dss), or brute-force attempts, the script should print `EVIL: <filename>`.
   - The script must be executable (`chmod +x`).

3. **Service Management**:
   We need this monitor to be part of our automated CI/CD pipeline environment. Create a `supervisord` configuration file at `/home/user/supervisord.conf` that manages a process named `ssh_monitor_daemon`. 
   - Since the monitor script is currently a batch processor, for the daemon configuration, simply set it to run `/home/user/ssh_monitor.py /app/incoming_logs` (you can assume `/app/incoming_logs` exists for the daemon).
   - Configure it so it auto-restarts if it crashes, writing logs to `/home/user/daemon.log`.

Do not attempt to run `sudo` as you do not have root access. Ensure your Python script is strictly named `/home/user/ssh_monitor.py` and expects exactly one positional argument (the directory path).