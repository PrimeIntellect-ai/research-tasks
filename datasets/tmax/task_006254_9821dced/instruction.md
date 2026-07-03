You are the on-call engineer responding to a 3 AM page. Our critical log processing pipeline has crashed in production, halting downstream billing updates. 

You have been given access to the failing environment. In the `/home/user/` directory, you will find:
- `parser.py`: The Python script responsible for extracting user IDs from incoming JSON log lines.
- `incoming_logs.txt`: The current batch of log lines that caused the crash.
- `crash_traceback.log`: The captured standard error output from the failed cron job.

The script is failing because the log format is occasionally malformed (invalid JSON) or missing expected nested keys. Currently, the script crashes completely on the first error, leaving the output incomplete.

Your task:
1. Analyze the traceback and the script to identify the failure points.
2. Modify `/home/user/parser.py` so that it handles parsing edge-cases gracefully. Specifically, if a line is invalid JSON or is missing the expected `event -> user -> id` path, the script should simply skip that line and continue processing the rest of the file.
3. Run your fixed `/home/user/parser.py` script to successfully process `/home/user/incoming_logs.txt`.
4. Ensure the output is written to `/home/user/extracted_users.txt` with exactly one user ID per line.

Do not change the input file; fix the script to be robust against bad data.