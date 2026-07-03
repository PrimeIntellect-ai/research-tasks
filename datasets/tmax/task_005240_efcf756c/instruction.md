You are a data analyst tasked with building an automated ETL pipeline that merges server event logs with system metric dumps. The pipeline must be written in Python, handle timestamp alignment, normalize text data, and be scheduled to run automatically.

Here are your requirements:

1. **Input Data**:
   - `/home/user/inputs/events.csv`: Contains columns `event_id`, `timestamp` (ISO 8601 strings, e.g., "2023-10-15T14:32:45Z"), and `raw_description`.
   - `/home/user/inputs/metrics.csv`: Contains columns `unix_time` (epoch seconds), `cpu_load` (float), and `ram_usage` (float).

2. **Transformations**:
   - **Timestamp Alignment**: Parse both time columns into UTC datetime objects. Truncate both to the start of the minute (e.g., `14:32:45` becomes `14:32:00`). Format the aligned timestamp as a string: `YYYY-MM-DD HH:MM:00`.
   - **Tokenization & Normalization**: Create a new column `action_token` from `raw_description`. Convert the description to lowercase, remove all punctuation (anything not a letter, number, or whitespace), and extract the *first* word as the `action_token`.
   - **Aggregation**: Group the metrics dataset by the aligned minute timestamp and calculate the mean of `cpu_load` and `ram_usage` for each minute. Round the averages to 2 decimal places.
   - **Merge**: Perform a left join from the events dataset to the aggregated metrics dataset using the aligned minute timestamp.

3. **Output**:
   - Save the joined dataset to `/home/user/output/merged_data.csv`.
   - The output CSV must have exactly these columns in this order: `minute_timestamp`, `event_id`, `action_token`, `avg_cpu`, `avg_ram`. Do not include an index column. If a metric is missing for a minute, leave it empty (standard CSV empty field).

4. **Pipeline Logging**:
   - Your Python script must append a log entry to `/home/user/logs/etl.log` every time it runs. 
   - Upon successful completion, it must append the exact string: `[YYYY-MM-DD HH:MM:SS] SUCCESS: Processed X events`, where `X` is the number of rows in the final merged CSV, and the timestamp is the current system time.

5. **Scheduling**:
   - Save your Python script at `/home/user/process_logs.py`.
   - Install a cron job for the current user (`user`) that runs this script every 15 minutes.

Please write the Python script, execute it once manually to generate the output files, and configure the cron job.