You are a log analyst investigating a recent spike in missing resources (HTTP 404 errors) on our web server. You need to extract, normalize, and anonymize this data so it can be safely shared with the development team for analysis.

I have placed a raw web server access log at `/home/user/access.log`.

Your task is to create a multi-stage Bash pipeline to process this log and produce a CSV report at `/home/user/analyzed_404s.csv`. You must use standard Linux CLI tools (like `awk`, `sed`, `grep`, etc.) to achieve this.

Requirements for the pipeline:
1. **Filter:** Extract only the log entries that resulted in an HTTP 404 status code.
2. **Anonymize:** Mask the IP address (the first field) by replacing the last octet with `0` (e.g., `198.51.100.17` becomes `198.51.100.0`).
3. **Normalize:** Extract the date from the timestamp `[DD/Mon/YYYY:HH:MM:SS +TZ]` and convert it to the standard `YYYY-MM-DD` format (e.g., `05/Nov/2023` becomes `2023-11-05`). You only need to handle the months present in the log.
4. **Extract:** Get the requested URL path from the request string (e.g., from `"GET /admin/config.php HTTP/1.1"`, extract `/admin/config.php`).
5. **Output Format:** Save the results to `/home/user/analyzed_404s.csv`. The file must include a header row: `IP,Date,URL`.
6. **Order:** Preserve the original chronological order of the entries as they appeared in the input log file.

Example output format for `/home/user/analyzed_404s.csv`:
```csv
IP,Date,URL
198.51.100.0,2023-11-05,/admin/config.php
```

Ensure your output matches this exact format, with no trailing spaces or extra quotes.