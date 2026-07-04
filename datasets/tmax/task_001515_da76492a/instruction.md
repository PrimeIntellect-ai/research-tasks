You are a log analyst investigating intermittent failure patterns across our infrastructure. You have received an exported CSV log file at `/home/user/raw_logs.csv`. However, the pipeline that generated this CSV mishandled embedded newlines, and the data is in a messy "wide" format with gaps. 

Write a Python script to process this file and generate a clean dataset and a summary report.

Here are the precise requirements for your script:

1. **Wide-to-Long Reshaping**: 
   Read `/home/user/raw_logs.csv`. The first column is `timestamp`, and the remaining columns are service names (`app_server`, `db_server`, `web_server`). Melt the data so that it has three columns: `timestamp`, `service`, and `message`. Drop any rows where the original message was completely empty/null.

2. **Normalization**:
   - Standardize service names to uppercase abbreviations: `app_server` -> `APP`, `db_server` -> `DB`, `web_server` -> `WEB`.
   - Clean the `message` field: Replace any embedded newline characters (`\n` or `\r\n`) with a single space. Strip any leading or trailing whitespaces from the resulting string.

3. **Hourly Aggregation & Gap-Filling**:
   - Convert `timestamp` to datetime and round down (floor) each timestamp to the nearest hour (e.g., `2023-10-01 10:15:00` becomes `2023-10-01 10:00:00`).
   - If there are multiple log messages for the same service in the same hour, combine them into a single string separated by `" | "`.
   - Create a continuous hourly time series for *each* service, starting from the overall minimum hour across all data, up to the overall maximum hour across all data.
   - Fill any resulting gaps (hours with no logs for a service) with the exact message `"NO_DATA"`.

4. **Rolling Statistics**:
   - Add a column named `error_count_3h`.
   - Determine if an hour's combined message contains the exact uppercase substring `"ERROR"`. (Count this as `1` if present, `0` if absent. `"NO_DATA"` obviously contains no errors).
   - Calculate the 3-hour rolling sum of these error presence indicators for each service independently. The window should include the current hour and the previous two hours (maximum possible value is 3). Use a minimum period of 1 (so the first hour's rolling sum is just its own error indicator).

5. **Processed Output**:
   Save the transformed data to `/home/user/processed_logs.csv`. It must contain the columns `timestamp`, `service`, `message`, and `error_count_3h`. The CSV should be sorted by `service` ascending, then `timestamp` ascending. Use standard comma delimiters and ensure timestamps are in `YYYY-MM-DD HH:MM:SS` format.

6. **Template Generation**:
   Generate a markdown report at `/home/user/report.md` summarizing the data. The file must exactly match this template structure:
   ```markdown
   # Service Report

   ## APP
   Max 3H Errors: <max_error_count_3h_for_APP>
   Latest Message: <message_for_the_maximum_timestamp_for_APP>

   ## DB
   Max 3H Errors: <max_error_count_3h_for_DB>
   Latest Message: <message_for_the_maximum_timestamp_for_DB>

   ## WEB
   Max 3H Errors: <max_error_count_3h_for_WEB>
   Latest Message: <message_for_the_maximum_timestamp_for_WEB>
   ```

Do not install any external libraries other than standard ones and `pandas`, which you may install using `pip install pandas` if needed. Run your script to produce the output files.