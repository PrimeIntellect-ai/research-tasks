You are an engineer tasked with building a tool to track configuration changes across our infrastructure. 

System audit logs are periodically archived in a staging directory. You need to retrieve the latest archive, write a high-performance C program to parse the custom log format, validate the entries, aggregate the changes into daily buckets, and generate a sorted report.

Here are your instructions:

1. **Environment Setup & Data Transfer**:
   - Create a working directory at `/home/user/workspace`.
   - Copy the staging archive from `/tmp/config_archive/audit_logs.tar.gz` to your working directory and extract it. It contains a file named `config_changes.log`.

2. **Log Format & Validation Checkpoint**:
   - The `config_changes.log` file contains text entries of configuration events. 
   - A valid log entry strictly follows this format:
     `[YYYY-MM-DDTHH:MM:SSZ] [USERNAME] [FILE_PATH] [ACTION] [SIZE_DIFF]`
     Example: `[2023-10-14T08:35:12Z] [admin] [/etc/nginx/nginx.conf] [MODIFIED] [+45]`
   - `SIZE_DIFF` is an integer representing bytes added or removed (e.g., `+45`, `-12`, `0`).
   - *Validation Gate*: Any line that does not strictly conform to this bracketed format (e.g., missing brackets, incomplete fields) is considered malformed and MUST be completely ignored by your parser.

3. **Data Transformation & Aggregation**:
   - Write a C program named `/home/user/workspace/config_analyzer.c`.
   - The program should take the input log file path and output CSV file path as command-line arguments: `./config_analyzer input.log output.csv`
   - It must parse the valid lines and extract the Date (the `YYYY-MM-DD` portion of the timestamp), the File Path, and the Size Diff.
   - Bucket the data by Date and group by File Path.
   - For each group (Date + File Path), calculate:
     - `TotalChanges`: The number of times this file was changed on this date.
     - `NetSizeDiff`: The sum of all `SIZE_DIFF` values for this file on this date.

4. **Sorting and Output**:
   - The C program must write the aggregated data to a CSV file.
   - The CSV must include a header row: `Date,FilePath,TotalChanges,NetSizeDiff`
   - The rows must be sorted chronologically by `Date` (ascending). If multiple files changed on the same date, sort those rows alphabetically by `FilePath` (ascending).

5. **Execution**:
   - Compile your C program using `gcc` and run it against the extracted `config_changes.log` to generate `/home/user/workspace/report.csv`.