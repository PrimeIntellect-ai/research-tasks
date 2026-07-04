You are a data engineer building an ETL pipeline to process global telemetry logs. You have received a raw log file containing irregular server metrics and multilingual error messages.

Your task is to write a shell script at `/home/user/process_telemetry.sh` that processes `/home/user/raw_telemetry.csv` and outputs the results to `/home/user/processed_telemetry.csv`.

**Input Format (`/home/user/raw_telemetry.csv`):**
A CSV file without a header. The columns are:
1. `epoch_sec` (integer): Unix timestamp in seconds.
2. `region` (string): Region identifier (e.g., "US", "EU", "JP").
3. `latency_ms` (float): Server latency in milliseconds.
4. `error_message` (string): A UTF-8 encoded error message (can contain non-ASCII characters, such as Japanese or German text). Can be empty.

**Processing Requirements:**
1. **Resampling:** Group the data by `region` and 1-minute intervals. To do this, floor the `epoch_sec` to the nearest multiple of 60 to get the `minute_epoch`.
2. **Aggregation:** If a minute has multiple records for a region, calculate the arithmetic mean of the `latency_ms` for that minute. Also, calculate the total number of UTF-8 *characters* (not bytes) across all `error_message` strings in that minute for that region.
3. **Gap-Filling:** For each region, find the minimum and maximum `minute_epoch`. If there are any missing 1-minute intervals between the min and max for that region, create a row for it. Forward-fill the aggregated `latency_ms` from the most recent available minute. The `total_error_chars` for a gap-filled minute should be `0`.
4. **Rolling Statistics:** Calculate a 5-minute rolling average of the aggregated/filled `latency_ms` for each region. The rolling window includes the current minute and up to 4 preceding minutes (e.g., if you are at minute $M$, average the latencies for $M, M-60, M-120, M-180, M-240$). If fewer than 5 minutes of history exist (at the beginning of a region's timeline), average the available minutes.
5. **Sorting:** Sort the final output alphabetically by `region` (ascending), and then by `minute_epoch` (ascending).

**Output Format (`/home/user/processed_telemetry.csv`):**
A CSV file without a header, containing the following columns:
`minute_epoch,region,resampled_latency,rolling_5m_avg,total_error_chars`

**Formatting details:**
- `resampled_latency` and `rolling_5m_avg` should be rounded to exactly 2 decimal places (e.g., `110.00`, `155.33`).
- `total_error_chars` must correctly count characters (e.g., "タイムアウト" is 5 characters, not 15 bytes).
- Ensure your script `/home/user/process_telemetry.sh` has executable permissions (`chmod +x`). You may use Bash, Awk, Python, or any combination of standard Linux tools within this script to accomplish the task.

Run your script to generate `/home/user/processed_telemetry.csv` when done.