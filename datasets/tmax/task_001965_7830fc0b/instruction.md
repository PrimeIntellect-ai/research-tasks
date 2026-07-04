You are an operations engineer investigating performance patterns from a high-throughput API gateway. We have a raw text log file that requires strict validation, time-based bucketing, and summary aggregations to identify potential bottlenecks.

Your task is to write a standard C program (saved as `/home/user/analyze_logs.c`) that parses a log file, filters invalid entries, aggregates the data by hour, and outputs the results to a CSV file.

**Input Log Format**
The input file is located at `/home/user/server.log`.
Each line is pipe-separated (` | `) with the following 5 fields:
`TIMESTAMP | IP_ADDRESS | LEVEL | DURATION_MS | ENDPOINT`
Example line: `2023-10-15T14:32:01Z | 192.168.1.100 | INFO | 145 | /api/v1/login`

**Processing Rules**
1. **Validation (Filtering):** You must ignore/skip any log line that meets ANY of the following conditions:
   - `LEVEL` is NOT exactly `INFO`, `WARN`, or `ERROR` (e.g., skip `DEBUG`, `TRACE`).
   - `DURATION_MS` is less than or equal to 0.
   - `ENDPOINT` does NOT start with the exact string `/api/`.
2. **Time-based Bucketing:** Extract the "Hour Bucket" from the `TIMESTAMP`. The hour bucket is the first 13 characters of the timestamp (e.g., `2023-10-15T14:32:01Z` becomes `2023-10-15T14`).
3. **Aggregation:** Group the valid log entries by `Hour Bucket` and `ENDPOINT`. For each group, calculate:
   - `count`: Total number of valid requests.
   - `avg_duration`: Average duration in milliseconds (integer arithmetic, floored).
   - `max_duration`: The maximum duration in milliseconds.

**Output Requirements**
Compile your C program to `/home/user/analyze_logs` and execute it.
It must write its output to `/home/user/summary.csv`.
The CSV must have the following exact header:
`hour_bucket,endpoint,count,avg_duration,max_duration`

The rows must be sorted alphabetically by `hour_bucket` ascending, and then by `endpoint` ascending.

Write, compile, and run your C code to produce `/home/user/summary.csv`. Do not use external libraries other than the standard C library (libc).