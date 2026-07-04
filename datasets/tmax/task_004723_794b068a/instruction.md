You are an infrastructure engineer automating the provisioning of a monitoring and reporting server. We have a daily workflow that extracts error log timestamps from diagnostic video captures of server consoles, formats them according to our company's specific locale and timezone, and emails a report to the admin mailing list.

You must complete three objectives:

1. **Idempotent Environment Setup**:
Write an idempotent bash script `/home/user/setup_env.sh` that:
- Configures the local system timezone to `Asia/Tokyo`.
- Generates and sets the system locale to `ja_JP.UTF-8`.
- Installs and configures a local `postfix` SMTP server (running on port 25) to act as a local mail relay. It should accept local unauthenticated mail and be configured to alias `admins@localhost` to the local user `user`.
- Ensures the postfix service is running. This script must be safely re-runnable without causing errors or duplicating configurations.

2. **Video Log Extraction**:
A diagnostic video file is located at `/app/diagnostic_console.mp4`. This video shows a terminal scrolling through boot logs. Using `ffmpeg` and OCR (or manual frame inspection logic if you prefer writing a script), extract the 5 unique error timestamps visible on the screen. The timestamps in the video are in UTC. Write these raw UTC timestamps to `/home/user/raw_timestamps.txt`, one per line, in the format `YYYY-MM-DD HH:MM:SS`.

3. **Log Formatter Program**:
Write a C++ program `/home/user/log_formatter.cpp` and compile it to `/home/user/log_formatter`.
This program must read lines from standard input. Each line will contain a single UTC timestamp in the format `YYYY-MM-DD HH:MM:SS`.
For each input line, the program must output the exact equivalent time in the `Asia/Tokyo` timezone, formatted using the `ja_JP.UTF-8` locale's standard date and time representation (using `strftime` with `%c` equivalent for that locale, or formatted exactly as: `YYYY年MM月DD日 HH時MM分SS秒`).
If the input string does not exactly match the `YYYY-MM-DD HH:MM:SS` format or represents an invalid date, output exactly `INVALID_FORMAT` on a new line.

Your C++ program will be rigorously tested against an extensive set of edge cases to ensure it precisely matches our legacy reference parser.

Finally, write a script `/home/user/send_report.sh` that pipes `/home/user/raw_timestamps.txt` through your `/home/user/log_formatter`, saves the output to `/home/user/formatted_report.txt`, and emails the contents of `/home/user/formatted_report.txt` to `admins@localhost` with the subject "Daily Log Report".