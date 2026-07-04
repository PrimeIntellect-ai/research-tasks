You are a monitoring specialist tasked with fixing and deploying a custom Rust-based alerting tool. 

The tool, located at `/app/log-alerter`, is designed to parse a large web access log (`/app/large_access.log`), find lines containing the string `CRITICAL_ERROR`, write a summary to an alerts directory, and send an alert email to a local SMTP server.

Currently, the automated setup is broken in several ways:
1. **Performance**: The tool is currently taking over 10 seconds to process the log file. You need to optimize it. The automated test will verify that the tool processes the log file in under 1.5 seconds. You may modify the Rust code or the build process.
2. **Environment/Path issues**: The wrapper script `/home/user/monitor.sh` simulates a stripped-down cron environment. Because of missing environment variables and relative path assumptions, the Rust tool is failing to write its output to the correct location (`/home/user/alerts/summary.log`). You must fix `/home/user/monitor.sh` and/or the Rust code so that the output file is consistently written to `/home/user/alerts/summary.log`.
3. **Mailing setup**: The tool attempts to send an email via SMTP to `127.0.0.1:2525`. There is currently no mail server running. You must start a lightweight background SMTP server (e.g., using Python) on port 2525 that accepts these emails and appends them to `/home/user/emails.log`.

Requirements:
- Fix the Rust package and run `make` inside `/app/log-alerter` to build the binary.
- Ensure the binary is placed at `/app/log-alerter/target/release/log-alerter` (or debug, depending on your fix, but it must be fast enough).
- Update `/home/user/monitor.sh` so that when run via `env -i bash /home/user/monitor.sh`, it correctly executes the Rust binary and produces `/home/user/alerts/summary.log`.
- Leave a background process running on port 2525 that captures emails to `/home/user/emails.log`.

Do not change the format of the output log or the email contents, only fix the performance, paths, and routing.