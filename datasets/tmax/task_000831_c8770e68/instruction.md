You are a log analyst investigating suspicious access patterns in our time-series logs. Our data pipeline processes JSON-lines (JSONL) log files, normalizes their timestamps, and bulk imports them into a SQLite database. 

However, we are facing two distinct problems:
1. Attackers are injecting malformed unicode escape sequences (specifically terminal escape codes like `\u001b` and `\u001B`) and invalid timestamps to break our downstream parsers.
2. The internal bulk import tool we use is currently broken due to a misconfiguration in its source code.

Your objectives:

**Part 1: Fix the Vendored Package**
We vendor our database loader tool at `/app/vendor/sqlite_bulk_loader-1.0.0`. The tool provides a script `install.sh` and an executable `load_csv.sh`. However, the package contains a deliberate perturbation (a broken Makefile and hardcoded wrong paths) which prevents it from running successfully and creating the database at `/home/user/metrics.db`.
- Fix the package in `/app/vendor/sqlite_bulk_loader-1.0.0` so that running `make install` works, and using `./load_csv.sh <input_file.csv>` correctly loads data into `/home/user/metrics.db`.

**Part 2: Create a Log Sanitizer**
Write an executable program or script at `/home/user/sanitize_logs` (you may use any language, e.g., Python, Bash, Node, etc.). It must read JSONL from `stdin` and output comma-separated values (CSV) to `stdout`.
For each JSON line:
- Parse the JSON. If it is malformed, drop the line.
- Check the `message` field. If it contains any unicode escape sequences for the escape character (i.e., `\u001b` or `\u001B` or the literal ESC character `\x1b`), drop the entire line.
- Read the `timestamp` field. It can be in various standard formats (e.g., epoch, ISO8601 with/without timezone). Parse it, and normalize it to exactly the format: `YYYY-MM-DDTHH:MM:SSZ` (UTC). If the timestamp is missing or unparseable, drop the line.
- Extract the `user_id` (integer) and `action` (string).
- Output the valid lines to `stdout` in CSV format without a header line. The columns must be exactly: `timestamp,user_id,action,message`.

**Verification:**
Your sanitizer at `/home/user/sanitize_logs` will be strictly evaluated against two distinct corpora of log files (you do not have access to these during development, so test your logic thoroughly):
- A "clean" corpus of perfectly valid JSON lines. Your script MUST preserve and output exactly 100% of these lines, properly normalized.
- An "evil" corpus containing injected control characters, bad unicode escapes, invalid JSON, and unparseable timestamps. Your script MUST reject 100% of the evil lines.

Finally, process a sample log file if you create one, pipe it through your sanitizer, and use the fixed `load_csv.sh` to ensure it successfully populates `/home/user/metrics.db`.