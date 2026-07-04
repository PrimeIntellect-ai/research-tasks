You are a data engineer responsible for building a lightweight ETL pipeline on an edge device. The device generates raw telemetry logs, and your task is to write a C program to parse, validate, and aggregate this data, then schedule it to run automatically.

Here are your requirements:

1. **Input Data**
   A log file is located at `/home/user/raw_data.log`. Each line has the following format:
   `LOG_TIME:<YYYY-MM-DDTHH:MM:SSZ> | SID:<SENSOR_ID> | VAL:<FLOAT_VALUE>`
   Example: `LOG_TIME:2023-10-15T10:05:23Z | SID:S01 | VAL:23.5`

2. **Data Processing (Write a C program)**
   Write a C program at `/home/user/etl_processor.c` and compile it to `/home/user/etl_processor`. The program must read `/home/user/raw_data.log` and do the following:
   - **Extraction**: Parse the timestamp, sensor ID (3 characters), and float value.
   - **Validation**: Discard any record where the `VAL` is less than `0.0` or greater than `100.0`.
   - **Time-based Bucketing & Aggregation**: Group the valid records into 15-minute tumbling windows based on the log time (e.g., `:00:00` to `:14:59` belongs to the `:00` bucket, `:15:00` to `:29:59` to the `:15` bucket, etc.). Calculate the average `VAL` for each sensor in each bucket.
   
3. **Output Format**
   The C program must create or overwrite `/home/user/summary.csv` with the aggregated results.
   - Format: `YYYY-MM-DDTHH:MM:00Z,SID,AVERAGE_VAL`
   - The timestamp should represent the *start* of the 15-minute bucket.
   - The average value must be formatted to exactly 2 decimal places (e.g., `21.50`).
   - Order the output chronologically by bucket start time, and then alphabetically by `SID`.

4. **Pipeline Scheduling**
   Configure a cron job for the current user (`user`) that executes `/home/user/etl_processor` exactly every 15 minutes (i.e., at minutes 0, 15, 30, and 45 of every hour).

Ensure your C code handles the file I/O safely and cleans up resources. You may use standard C library functions (e.g., `stdio.h`, `string.h`, `stdlib.h`). Compile your code using `gcc`.