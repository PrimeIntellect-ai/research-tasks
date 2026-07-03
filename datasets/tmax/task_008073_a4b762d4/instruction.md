You are tasked with building an automated backup restore testing system. As a backup operator, you need to regularly ensure that generated backup archives can be successfully extracted and that their contents are healthy.

You must implement a solution using Go and Bash, consisting of three parts:

1. **Go Restore Tester (`/home/user/restore_tester.go`)**
Write a Go program that simulates testing a batch of backup archives.
- The program must find all `.tar.gz` files in `/home/user/backups/`.
- For each archive, extract its contents into a temporary directory: `/home/user/tmp_restore/<archive_basename>/` (for example, extract `backup_1.tar.gz` into `/home/user/tmp_restore/backup_1/`). You can assume standard `tar` command is available or use Go's `archive/tar`. Calling the system `tar -xzf` is highly recommended for simplicity.
- Inside each extracted archive, look for a file named `meta.json` at the root of the extracted folder.
- Parse `meta.json`. It will contain a JSON object with a `status` key (e.g., `{"status": "ok"}`).
- A backup is considered successful ONLY if `meta.json` exists, is valid JSON, and its `status` field is exactly `"ok"`. Otherwise (missing file, invalid JSON, or different status), it is considered a failure.
- The program must write the results to `/home/user/restore_results.log`. The output must be sorted alphabetically by the original archive filename. The format for each line must be exactly: `filename.tar.gz,STATUS` where `STATUS` is either `SUCCESS` or `FAILED`.
- The program must clean up (delete) the `/home/user/tmp_restore/` directory completely before exiting.

2. **Wrapper Bash Script (`/home/user/run_tester.sh`)**
Write a robust bash script to execute the testing process.
- The script must build the Go program: `go build -o /home/user/restore_tester /home/user/restore_tester.go`.
- If the Go build fails, the script must write the exact string `BUILD_FAILED` as a single line to `/home/user/restore_results.log` and exit with status code `1`.
- If the build succeeds, it should execute the compiled `/home/user/restore_tester` binary and exit with status code `0`.
- Ensure the script has executable permissions.

3. **Scheduled Task Configuration (`/home/user/cron.conf`)**
Create a cron configuration file at `/home/user/cron.conf`.
- The file should contain a single valid crontab line that schedules `/home/user/run_tester.sh` to run every 15 minutes. Use `*` for fields where applicable, but ensure the step value or list correctly specifies every 15 minutes.

Do not manually create the log file or run the script; your deliverables are the Go source code, the Bash script, and the cron configuration file.