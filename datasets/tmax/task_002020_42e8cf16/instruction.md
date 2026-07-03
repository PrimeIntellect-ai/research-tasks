You are an administrator tasked with setting up a secure user account monitoring dashboard. The previous administrator left behind a partially working setup, but the automated cron jobs keep failing due to working directory environment differences.

You need to fix the existing C monitoring tool, automate user creation using `expect`, and expose the generated report securely via a user-level `systemd` service.

Here is your to-do list:

1. **Fix the C Monitoring Tool:**
   There is a C source file at `/home/user/account_monitor.c`. It reads `/home/user/users.db` and writes an HTML report to `/home/user/public_html/report.html`. However, the current code uses relative paths (`"users.db"` and `"public_html/report.html"`). Because it is frequently triggered by a script that runs from `/tmp`, it fails to find the files.
   - Modify `/home/user/account_monitor.c` to use the absolute paths `/home/user/users.db` and `/home/user/public_html/report.html`.
   - Compile the program to `/home/user/account_monitor`.
   - Ensure the output directory `/home/user/public_html` exists.

2. **Automate User Creation:**
   There is an interactive script at `/home/user/interactive_admin.sh`. It prompts for `Enter new username: ` and then `Enter password: `, before saving the data to the database.
   - Write an Expect script at `/home/user/add_user.exp` that automates running `/home/user/interactive_admin.sh`.
   - The expect script must add the username `charlie` with the password `secure_pass_123`.
   - Execute your Expect script so that `charlie` is successfully added to `/home/user/users.db`.
   - Once the user is added, manually run your compiled `/home/user/account_monitor` to generate the latest report.

3. **Secure Web Server Configuration:**
   - Generate a self-signed TLS certificate and key in `/home/user/certs/` (name them `cert.pem` and `key.pem`).
   - Write a simple Python script at `/home/user/tls_server.py` that serves the contents of `/home/user/public_html` over HTTPS on `0.0.0.0` port `8443`.
   - Create a systemd user service named `monitor-web.service` (placed in `/home/user/.config/systemd/user/`) that runs `/home/user/tls_server.py`.
   - Start and enable the service using `systemctl --user`.

Verify your setup by ensuring `curl -k https://localhost:8443/report.html` returns the generated HTML report containing the user `charlie`.