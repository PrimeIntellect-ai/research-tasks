You are a log analyst investigating error patterns across different system components. The logs are stored in multiple formats, and your goal is to extract, normalize, and aggregate error occurrences to generate an HTML report.

You have been provided with two log files:
1. `/home/user/logs/app.json`: JSON format logs. Each line is a JSON object with keys `timestamp` (format `YYYY-MM-DDTHH:MM:SSZ`), `level`, and `message`.
2. `/home/user/logs/sys.csv`: CSV format logs. Columns are `timestamp` (format `YYYY-MM-DD HH:MM:SS`), `level`, and `message`.

There is also an HTML template at `/home/user/template.html`.

Your task is to write and execute a Bash script (save it as `/home/user/analyze.sh`) that performs the following:
1. Reads both log files and filters for log entries where the `level` is exactly `"ERROR"`.
2. Normalizes the timestamps to extract just the date and hour in the format `YYYY-MM-DD_HH`.
3. Tokenizes the `message` field to extract the exact error code. Error codes are always enclosed in square brackets in the message (e.g., `[ERR-001]`). You should extract just the code (e.g., `ERR-001`).
4. Aggregates the data to find the count of each unique error code per hour.
5. Generates HTML table rows for the aggregated data in the exact format: `<tr><td>HOUR</td><td>ERROR_CODE</td><td>COUNT</td></tr>`. The rows must be sorted chronologically by HOUR, and then alphabetically by ERROR_CODE.
6. Replaces the placeholder `__TABLE_ROWS__` in `/home/user/template.html` with the generated rows, saving the final output to `/home/user/report.html`.

Ensure your script is executable and run it so that `/home/user/report.html` is created. Do not change the rest of the template.