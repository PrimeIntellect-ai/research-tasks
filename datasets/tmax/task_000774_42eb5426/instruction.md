You are an operations engineer triaging a recent incident. A nightly cron job that processes timezone data occasionally fails, but the logs don't specify which input caused the failure. 

You have been given a Python script located at `/home/user/process_time.py` which takes a single date-time string as an argument (format: `YYYY-MM-DD HH:MM`). It converts the local time (`America/Chicago`) to UTC and does some processing. Due to a subtle bug related to daylight saving time transitions, it crashes and returns a non-zero exit code for specific ambiguous or non-existent times.

You also have a file `/home/user/timestamps.txt` containing 500 different timestamps, one per line. 

Your task:
1. Write a shell loop or use bash utilities to "fuzz" or systematically test the `process_time.py` script with every timestamp in `/home/user/timestamps.txt`.
2. Identify the exact timestamp that causes the script to crash (return a non-zero exit code).
3. Write ONLY the crashing timestamp (exactly as it appears in the text file) to a new file at `/home/user/solution.txt`.

You must accomplish this using standard Linux terminal commands (bash, xargs, etc.).