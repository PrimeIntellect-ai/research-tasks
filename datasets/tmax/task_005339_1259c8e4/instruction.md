You are a monitoring specialist tasked with setting up a secure alert and logging pipeline for a network gateway. We have been observing malicious login attempts that exploit a vulnerability in our downstream log parser by injecting shell metacharacters into the SSH key fingerprint field, leading to "silent rejections" where the connection drops but the backend crashes.

We use a proprietary, stripped binary located at `/app/ssh_auditor`. This binary reads raw authentication logs from standard input and outputs a normalized, pipe-separated (`|`) string containing connection metadata. You will need to run this binary with some sample inputs to deduce its exact output format.

Your task is to build a robust pipeline that sanitizes these logs and sets up appropriate permissions and rotation.

**Requirements:**

1. **C++ Sanitizer (`/home/user/sanitizer.cpp` & `/home/user/sanitizer`)**
   Write and compile a C++ program that reads the output of `/app/ssh_auditor` line-by-line from standard input.
   - It must act as a filter.
   - It should parse the pipe-separated fields.
   - It MUST drop (reject) any line where the `METHOD` field is `publickey` AND the `FINGERPRINT` field contains any of the following shell metacharacters: `;`, `|`, `&`, `$`, `>`, or `<`.
   - All other valid lines (clean logs) must be printed to standard output exactly as they were received.

2. **Pipeline Script (`/home/user/process_logs.sh`)**
   Write a robust bash script that takes a single file path as an argument.
   - It must read the specified raw log file.
   - Pipe the contents into `/app/ssh_auditor`.
   - Pipe the output of the auditor into your `/home/user/sanitizer`.
   - Append the final clean output to `/home/user/alerts/sanitized_ssh.log`.

3. **Permissions & Security**
   - Create the directory `/home/user/alerts`.
   - Ensure the directory has `0700` permissions.
   - Ensure `/home/user/alerts/sanitized_ssh.log` has `0600` permissions.

4. **Log Rotation (`/home/user/logrotate.conf`)**
   Create a logrotate configuration file at `/home/user/logrotate.conf` specifically for `/home/user/alerts/sanitized_ssh.log`.
   - It must rotate the log `daily`.
   - Keep `7` days of backlogs.
   - `compress` old logs.
   - Recreate the log file with `0600` permissions.

Ensure all scripts and code are executable and properly compiled.