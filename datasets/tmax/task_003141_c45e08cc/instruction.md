You are a data engineer responsible for processing incoming IoT sensor telemetry. 

You have been given a directory `/home/user/data` containing two raw log files:
1. `/home/user/data/sensor_a.csv` (Encoded in UTF-16LE)
2. `/home/user/data/sensor_b.csv` (Encoded in ISO-8859-1)

Both CSV files contain a header row: `time,device,value,status`. 
Some status fields contain non-ASCII characters (e.g., the degree symbol `°`).

Your task is to write and execute a Bash script that performs the following ETL pipeline and outputs the final result to `/home/user/processed.csv`.

Pipeline Requirements:
1. **Encoding Normalization**: Read both files and convert their contents to pure UTF-8.
2. **Merge and Sort**: Combine the records from both files and sort them chronologically (ascending) by the `time` column.
3. **Deduplication**: Deduplicate the records based on the payload. A record is considered a duplicate if it has the exact same `device`, `value`, and `status` as a previously seen record (ignoring the `time`). If duplicates exist, keep only the *first* chronological occurrence and drop the subsequent ones.
4. **Rolling Statistics**: For each unique `device`, compute a rolling average of the `value` column over a window of the last 3 chronological records (including the current record). If a device has fewer than 3 records at that point in time, average the available ones. 
5. **Output Formatting**: The final file `/home/user/processed.csv` must be encoded in UTF-8, comma-separated, and include a new header: `time,device,value,status,rolling_avg`. Format the `rolling_avg` to exactly one decimal place (e.g., `12.0`).

Complete the task using Bash shell commands and standard Unix utilities (like `iconv`, `awk`, `sort`, `sed`, etc.). Write your logic into a script if needed, but ensure `/home/user/processed.csv` is created with the exact requested format and data.