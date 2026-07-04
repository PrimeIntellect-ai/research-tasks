You are a log analyst investigating a recent series of failures across our international servers. You need to parse, merge, and aggregate multi-lingual log files using Bash.

We have two log files from different regional servers:
1. `/home/user/server_A/app.log`
2. `/home/user/server_B/app.log`

The log format is: `YYYY-MM-DDThh:mm:ssZ [LEVEL] MESSAGE`
For example: `2023-10-12T14:32:01Z [ERROR] Base de données hors ligne`

Your task is to write a Bash script or command pipeline that does the following:
1. Merges the logs from both servers.
2. Filters the logs to keep only `[ERROR]` and `[CRITICAL]` level messages.
3. Buckets the timestamps down to the hour, formatting it as `YYYY-MM-DD_HH`.
4. Extracts the error message (everything after the log level, stripping leading spaces).
5. Counts the frequency of each unique `(Hour, Message)` combination.
6. Outputs the results to a comma-separated values (CSV) file at `/home/user/error_summary.csv`.
7. The CSV must have the header: `Hour,Message,Count`
8. The rows must be sorted chronologically by `Hour` (ascending), and then by `Count` (descending) within each hour. If counts are tied, sort alphabetically by `Message`.

Notes:
- The log messages contain UTF-8 encoded text in multiple languages (French, German, Japanese, English). Your tools must handle Unicode correctly.
- Do not use external scripting languages like Python or Perl; stick to standard Linux text processing utilities (awk, sed, grep, sort, uniq, etc.) within Bash.