You are a log analyst investigating performance patterns on our servers. You have been given a large JSON-Lines log file located at `/home/user/server_logs.jsonl`.

However, the file has a few issues that require a careful data processing pipeline using Bash, coreutils, and standard CLI tools (`sed`, `awk`, `jq`, etc.):

1. **Corrupted JSON / Tokenization issue:** A legacy module occasionally injects invalid hex escape sequences (e.g., `\x2F`, `\xA9`) into the `message` field of the JSON logs. Standard JSON parsers like `jq` will fail to parse these lines. You must stream the file and clean these invalid `\xNN` sequences (where `N` is any hex digit 0-9, a-f, A-F) by removing them entirely before parsing.
2. **Feature Extraction:** From the cleaned JSON stream, extract the `timestamp`, `user_id`, and `response_time_ms` fields.
3. **Imputation:** Occasionally, the `response_time_ms` is `null`. You must impute this missing data. If a `response_time_ms` is missing, replace it with the *last known valid response time* for that specific `user_id`. If this is the first request for a user and it is missing, use `0` as the imputed value.
4. **Windowed Aggregation:** For each `user_id`, calculate a rolling average of the `response_time_ms` (using the imputed values when necessary) over the last 3 requests for that user. If the user has fewer than 3 requests so far, calculate the average using the available requests (1 or 2).

Write a Bash script (or pipeline) that processes the file line-by-line (to support large-file streaming) and outputs the results as a CSV file to `/home/user/analyzed_logs.csv`.

**Output Format Constraints:**
The output CSV must have exactly four columns in this order: `timestamp,user_id,response_time_ms,rolling_avg_3`.
- `response_time_ms` should be an integer.
- `rolling_avg_3` must be formatted as a floating-point number rounded to exactly 2 decimal places (e.g., `125.00`, `133.33`).
- Do not include a CSV header row.

Your solution should not load the entire file into memory at once (use pipes). Create the final `/home/user/analyzed_logs.csv` file to complete the task.