You are a log analyst investigating patterns in system errors. You have been given a large CSV log file at `/home/user/system_logs.csv` containing fields: `timestamp`, `level`, `service`, and `message`. 

However, the logging system sometimes includes embedded newline characters inside the quoted `message` field, which breaks simple line-by-line bash processing tools. Also, the `level` field is inconsistently cased (e.g., "Error", "ERROR", "error", "Warning").

Your task is to write an executable bash script at `/home/user/process_logs.sh` that acts as a pipeline to:
1. Stream and parse `/home/user/system_logs.csv` correctly, properly handling embedded newlines within the quoted `message` fields by replacing those embedded newlines with a single space.
2. Normalize the `level` column so that all values are uppercase.
3. Filter the stream to keep only rows where the normalized `level` is exactly `ERROR`.
4. Aggregate the counts of `ERROR` logs per `service`.
5. Output the final aggregated results to `/home/user/error_counts.csv` with the header `service,count`, sorted alphabetically by the `service` name.

Your script must process the file efficiently (streaming) and must not load the entire file into memory at once, as the real file could be massive. You may use standard Unix tools, AWK, Perl, or Python within your bash script to handle the CSV parsing properly.

Run your script to ensure `/home/user/error_counts.csv` is generated correctly.