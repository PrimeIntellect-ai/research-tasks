You are a data engineer responsible for building a strict ETL pipeline that ingests raw IoT sensor data, validates constraints, resamples the data to fill missing gaps, and generates a formatted text report. 

You must write a Rust program to handle this process. 

**Part 1: Fix the Vendored Package**
We have a local vendored package located at `/app/vendor/gap_filler`. It contains an essential Rust library intended to aid in pipeline tasks. However, it currently fails to compile due to an environmental configuration issue (a deliberately broken `build.rs` expecting an incorrectly named environment variable `GAP_FILL_BUILD_TOKEN` that is not exported anywhere in the system, whereas the environment actually provides `BUILD_TOKEN="SECURE"`). 
Your first task is to fix the `gap_filler` package so that it compiles successfully.

**Part 2: Build the ETL Pipeline**
Create a new Rust project at `/home/user/etl_pipeline`. Add the fixed `/app/vendor/gap_filler` as a local dependency. 

Write a Rust CLI application (`src/main.rs`) that reads raw CSV data from `stdin` until EOF. 
The input CSV has no header and contains three columns:
`timestamp_sec,sensor_id,value`
(e.g., `1600000005,sensorA,45`)
- `timestamp_sec`: UNIX epoch in seconds (integer)
- `sensor_id`: string (alphanumeric)
- `value`: integer

**Pipeline Requirements:**
1. **Constraint Validation:** Discard any row where `value` is less than 0 or greater than 1000.
2. **Resampling & Gap-filling:** Group the data by `sensor_id`. For each sensor, find the minimum valid timestamp and maximum valid timestamp, and round both *down* to the nearest 60-second boundary (e.g., `1600000005` becomes `1600000000`). 
   - For every 60-second bucket from the minimum to the maximum bucket (inclusive), determine the *maximum* valid `value` that fell exactly within that `[bucket, bucket + 59]` window.
   - If a 60-second bucket has no valid input rows, carry forward the maximum value from the immediate previous bucket.
3. **Template-based Generation:** For each bucket generated, print exactly the following template to `stdout`:
   `REPORT: Sensor <sensor_id> at <bucket_timestamp> has max value <value>`
4. **Ordering:** The final output printed to `stdout` must be sorted lexicographically by `sensor_id` (ascending), and then chronologically by `bucket_timestamp` (ascending).

Compile your binary in release mode. The automated test will invoke `/home/user/etl_pipeline/target/release/etl_processor` by feeding it random generated CSVs via stdin and comparing the stdout byte-for-byte against a known reference oracle.