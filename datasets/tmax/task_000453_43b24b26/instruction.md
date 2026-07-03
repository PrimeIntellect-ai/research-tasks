You are a log analyst investigating server instability patterns. 

Our logging pipeline has been failing to properly aggregate error metrics because the raw log files contain embedded newlines in the stack traces, which breaks our naive line-by-line parsers. Furthermore, the logging agents on legacy servers output the CSV in UTF-16LE encoding.

I have placed a raw log file at `/home/user/raw_logs.csv`. 

Your task is to write a Python script that processes this file and produces a clean summary report at `/home/user/error_summary.csv`.

Here are the requirements for your processing:
1. **Handle Encoding and Newlines**: Read `/home/user/raw_logs.csv` correctly. It is a CSV file encoded in UTF-16LE. The columns are `local_time`, `timezone`, `server`, `error_category`, and `details`. The `details` column contains embedded newlines wrapped in quotes.
2. **Timestamp Alignment**: The `local_time` column is in the format `YYYY-MM-DD HH:MM:SS`. Convert this to UTC using the `timezone` column (e.g., `America/New_York`, `Asia/Tokyo`). 
3. **Filtering**: Only include log entries where the exact UTC time is on the date `2024-03-01` (i.e., from `2024-03-01T00:00:00Z` to `2024-03-01T23:59:59Z` inclusive).
4. **Reshaping and Aggregation**: Count the number of errors per `server` per `error_category` for the filtered timeframe. Transform this long format into a wide format where:
   - The first column is `server`.
   - The remaining columns are the unique `error_category` values (sorted alphabetically).
   - The values are the counts of errors. If a server has no errors of a particular category, the value must be `0`.
5. **Output**: Save the result to `/home/user/error_summary.csv`. The output file must be UTF-8 encoded. The rows must be sorted alphabetically by the `server` column.

Ensure your output is a strictly formatted CSV (comma-separated, with headers) so our automated tests can verify it. Do not include row indices.