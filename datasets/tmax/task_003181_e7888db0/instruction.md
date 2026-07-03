You are a localization engineer tasked with modernizing a legacy translation ETL pipeline. Our old pipeline relies on a compiled C binary (`/app/legacy_loc_etl`) that parses translation telemetry logs, but we need to migrate this step to Python while maintaining absolute bug-for-bug compatibility to pass our rigid regression tests.

Your objective is to write a Python script at `/home/user/loc_etl.py` that reads from `stdin` and writes to `stdout`, replicating the exact behavior of the legacy binary. 

The input is a stream of CSV data (without a header) with the following columns:
1. `timestamp` (integer Unix epoch)
2. `source_string` (text)
3. `translated_string` (text)

The legacy binary implements the following logic:
1. **The "Embedded Newline" Bug:** The legacy parser cannot handle embedded newlines. It silently drops any logical CSV row that contains an embedded newline character (even if properly quoted). You must replicate this flaw.
2. **Time-Based Bucketing:** It groups the remaining valid records into 5-minute (300 seconds) tumbling windows based on the `timestamp` (bucket = `timestamp - (timestamp % 300)`).
3. **Distance Computation:** For each valid row, it calculates the length difference: `distance = abs(len(source_string) - len(translated_string))`.
4. **Rolling Statistics:** It computes the rolling average of this `distance` for up to the last 3 valid records *strictly within the current time bucket*. If a record falls into a new time bucket, the rolling window is completely reset.
5. **Output Format:** For every valid record processed, it prints a single line to `stdout` containing the bucket timestamp and the rolling average formatted to exactly two decimal places, separated by a comma (e.g., `1700000300,12.50`).

To complete the pipeline scheduling requirement, you must also create a standard crontab file at `/home/user/sync_cron` that contains a rule to execute `python3 /home/user/loc_etl.py < /tmp/input.csv > /tmp/output.csv` every 15 minutes.

Ensure your Python script relies only on the standard library and accurately perfectly mirrors the binary's output.