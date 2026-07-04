You are a log analyst investigating resource usage patterns across different locales in an ETL pipeline. An issue with the ETL job retries has resulted in duplicate records in the log files.

Your task is to write a C++ program to process a large tab-separated values (TSV) log file, filter out the duplicates, and calculate summary statistics. 

Here are the details:
1. The input file is located at `/home/user/etl_logs.tsv`.
2. The TSV file has no header row. The columns are, in order: 
   `timestamp` (string), `transaction_id` (string), `lang` (string, e.g., 'en', 'es', 'zh'), `user_message` (UTF-8 string), `cpu_ms` (integer), `mem_mb` (integer), `net_kb` (integer).
3. **Filter Duplicates:** The file contains duplicate `transaction_id`s due to ETL retries. You must stream the file and process only the *first* occurrence of each `transaction_id`. Ignore any subsequent lines with a `transaction_id` you have already seen.
4. **Reshape and Aggregate:** For each unique transaction, reshape the wide resource columns (`cpu_ms`, `mem_mb`, `net_kb`) and compute the average (mean) value for each resource type, grouped by `lang`.
5. **Output:** Write the results to `/home/user/summary.csv`. The output must be a CSV file with a header: `lang,resource,avg_value`.
   - The `resource` column should contain the strings `cpu_ms`, `mem_mb`, or `net_kb`.
   - Sort the output alphabetically first by `lang`, and then by `resource`.
   - Format `avg_value` to exactly 2 decimal places (e.g., `15.50`).

Write your C++ code in `/home/user/analyze_logs.cpp`, compile it (e.g., to `/home/user/analyze_logs`), and run it to produce the `summary.csv` file. Ensure it is efficient enough to stream large files without loading the entire file into memory (though you may store IDs to track duplicates).