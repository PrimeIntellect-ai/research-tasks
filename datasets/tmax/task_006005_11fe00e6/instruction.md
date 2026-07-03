You are a data engineer tasked with building a high-performance, lightweight ETL (Extract, Transform, Load) processor in C. 

System metrics from our edge servers are accumulating in a custom, wide-format log file, but they are messy. Timestamps are inconsistently logged in either Unix Epoch seconds or ISO8601 format. You need to write a C program that extracts this data, normalizes the timestamps, detects anomalous system states, reshapes the data from wide to long format, and generates SQL insert statements based on a template.

The raw log file is located at: `/home/user/raw_logs.txt`. 
If it does not exist, assume it will be placed there before your compiled binary runs (though you should test with a sample).

Each line in the log file follows this space-separated format:
`[TIMESTAMP] [SERVER_ID] cpu:[VAL] mem:[VAL] disk:[VAL]`

**Example lines:**
`1696118400 SERVER_A cpu:45.2 mem:80.1 disk:50.0`
`2023-10-01T00:05:00Z SERVER_B cpu:95.0 mem:92.5 disk:88.0`

**Your ETL requirements:**
1. **Timestamp Alignment:** Parse the `[TIMESTAMP]`. It will either be an integer (Unix Epoch seconds) or a string in `YYYY-MM-DDThh:mm:ssZ` format. Convert both into a normalized UTC string in the format `YYYY-MM-DD HH:MM:SS`.
2. **Anomaly Detection:** Evaluate the metrics on each line. If *both* `cpu` > 90.0 AND `mem` > 90.0 on a single line, then the server is experiencing an anomaly. This state applies to all metrics extracted from that specific line.
3. **Wide-to-Long Reshaping:** For every log line, output exactly 3 separate records (one for cpu, one for mem, one for disk).
4. **Template-Based SQL Generation:** Write the reshaped records into an output file at `/home/user/etl_output.sql`. Each record must be formatted exactly as:
`INSERT INTO metrics (log_time, server, metric_name, metric_value, anomaly_flag) VALUES ('[NORMALIZED_TIME]', '[SERVER_ID]', '[METRIC_NAME]', [VALUE_TO_1_DECIMAL_PLACE], [1_OR_0_ANOMALY]);`

**Deliverables:**
1. Create a C source file at `/home/user/etl_processor.c`.
2. Compile it using standard `gcc` (you may use POSIX and standard C libraries like `<time.h>`, `<stdio.h>`, `<string.h>`, `<stdlib.h>`). The compiled binary should be at `/home/user/etl_processor`.
3. Run your program so that it reads `/home/user/raw_logs.txt` and produces `/home/user/etl_output.sql`.

*Note:* You must ensure exactly one decimal place for the floating point values in the SQL string (e.g., `45.2`, `90.0`). The `anomaly_flag` must be an integer, `1` if the line was an anomaly, otherwise `0`.

Write, compile, and execute the C program to satisfy these constraints.