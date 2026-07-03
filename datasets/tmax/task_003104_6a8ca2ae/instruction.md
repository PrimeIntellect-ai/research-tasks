You are a data engineer tasked with building a high-performance, C-based ETL pipeline component to process raw IoT sensor telemetry logs. 

You must write a C program and a Bash wrapper script to extract, validate, aggregate, and output the data, enforcing strict data quality rules.

**Input Data**
A raw text log file will be located at `/home/user/data/sensor_raw.log`.
Each line follows this format:
`[YYYY-MM-DDThh:mm:ssZ] SENSOR_LOG device=<DEVICE_ID> temp=<FLOAT> hum=<FLOAT>`

Example:
`[2023-10-12T10:15:30Z] SENSOR_LOG device=DEV01 temp=22.5 hum=45.0`

**Step 1: C Program (`/home/user/etl_processor.c`)**
Write a C program that reads the input log file path as its first command-line argument. The program must:
1. **Extract Structured Info:** Parse each line to extract the timestamp, `device`, `temp` (temperature), and `hum` (humidity).
2. **Constraint Validation:** A record is considered *VALID* only if:
   - `temp` is between `-50.0` and `150.0` (inclusive).
   - `hum` is between `0.0` and `100.0` (inclusive).
   Records failing these constraints are *INVALID* and should be dropped from aggregation.
3. **Time-Based Bucketing:** For all *VALID* records, truncate the timestamp to the start of the hour (e.g., `2023-10-12T10:15:30Z` becomes `2023-10-12T10:00:00Z`).
4. **Aggregation:** Calculate the average `temp` and average `hum` per hourly bucket per device.
5. **Output CSV:** Write the aggregated data to `/home/user/output/aggregated.csv`.
   - Format: `bucket,device_id,avg_temp,avg_hum`
   - Float precision: Exactly 2 decimal places (e.g., `23.45`).
   - Order: Sorted alphabetically by `bucket`, then by `device_id`.
6. **Pipeline Logging:** Write a summary log to `/home/user/output/etl.log` with exactly one line in this format:
   `TOTAL:<N> VALID:<V> INVALID:<I>`
   (where N, V, and I are the respective integer counts of records).

**Step 2: Quality Gate Wrapper (`/home/user/run_pipeline.sh`)**
Write a bash script that:
1. Compiles the C program (`gcc -O2 /home/user/etl_processor.c -o /home/user/etl_processor`).
2. Runs the compiled executable, passing `/home/user/data/sensor_raw.log` as the argument.
3. Reads `/home/user/output/etl.log` to determine the data quality.
4. **Quality Gate:** If the ratio of INVALID records to TOTAL records is strictly greater than `0.10` (10%), create an empty file at `/home/user/output/quality_gate_failed`. Otherwise, create an empty file at `/home/user/output/quality_gate_passed`.

**Requirements:**
- Ensure `/home/user/output/` directory is created if it doesn't exist.
- Standard C libraries only (no external dependencies like libcurl or jansson).
- Make sure `/home/user/run_pipeline.sh` is executable and run it to complete the task.