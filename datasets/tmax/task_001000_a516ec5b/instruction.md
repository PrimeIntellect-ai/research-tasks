You are a data engineer building a time-series ETL pipeline. We receive custom telemetry logs from our IoT edge devices. Recently, a firmware update caused some devices to inject unicode escape sequences (e.g., `\u2713`) into the "status" field, which is breaking our downstream analytics. Furthermore, our aggregations require timestamps to be aligned to the minute, and we need to filter out anomalous temperature spikes.

I have provided a workspace in `/home/user/`.
There is a raw data file located at `/home/user/data/telemetry.log`.
Each line in the log follows this exact format:
`TIMESTAMP | SENSOR_ID | TEMPERATURE | status="STATUS_STRING"`

For example:
`2023-10-12T08:14:55Z | S100 | 45.2 | status="active"`
`2023-10-12T08:15:12Z | S102 | 85.0 | status="overheating\u26A0"`

Your task is to write a C++ program at `/home/user/src/etl.cpp` that processes this log file and generates a clean CSV file at `/home/user/output/clean_telemetry.csv`.

Your pipeline must satisfy the following requirements:
1. **Timestamp Alignment:** Parse the ISO 8601 timestamp and align it to the floor minute (e.g., `2023-10-12T08:14:55Z` becomes `2023-10-12T08:14:00Z`).
2. **Constraint Validation:** Parse the temperature as a float. Filter out (drop) any records where the temperature is strictly less than `-20.0` or strictly greater than `60.0`.
3. **Unicode Handling (The Bug):** The `STATUS_STRING` may contain `\uXXXX` (where X is a hex digit). You must strip these 6-character escape sequences entirely from the extracted status string. (e.g., `overheating\u26A0` becomes `overheating`).
4. **Output Format:** Write the valid, cleaned, and aligned records to `/home/user/output/clean_telemetry.csv` as a standard CSV with the following header exactly as written:
   `timestamp,sensor,temperature,status`
   Followed by the data rows, keeping the temperature formatted to exactly 1 decimal place.

Example Output Row:
`2023-10-12T08:14:00Z,S100,45.2,active`

Compile your C++ program using `g++ -std=c++17 -O2 /home/user/src/etl.cpp -o /home/user/src/etl` and execute it to generate the output file.