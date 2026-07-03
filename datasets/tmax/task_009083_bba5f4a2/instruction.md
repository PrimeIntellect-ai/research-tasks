You are a data analyst setting up a reproducible data processing pipeline. You have a raw dataset of sensor readings, and you need to perform feature engineering using Rust for speed and safety.

Your task is to write and execute a Rust program that reads a CSV file, engineers new mathematical features, outputs the processed data, and logs the experiment to ensure reproducibility.

**Input Data:**
There is a CSV file located at `/home/user/data/raw_sensors.csv` with the following columns:
`timestamp` (integer)
`sensor_A` (float)
`sensor_B` (float)

**Requirements:**
1. Setup a new Rust project named `sensor_pipeline` in `/home/user/sensor_pipeline`.
2. Add the necessary dependencies (like `csv` and `serde`) to your `Cargo.toml`.
3. Write a Rust program in `src/main.rs` that reads `/home/user/data/raw_sensors.csv`.
4. Perform the following **Feature Engineering** for each row:
   - Calculate `diff`: `sensor_A` minus `sensor_B`.
   - Calculate `magnitude`: The Euclidean distance from the origin for the two sensors, which is the square root of (`sensor_A` squared + `sensor_B` squared). Round this to exactly 4 decimal places (e.g., `11.1803`).
5. Write the output to a new CSV file at `/home/user/data/features.csv`. The output CSV must have the following header and order:
   `timestamp,sensor_A,sensor_B,diff,magnitude`
6. **Experiment Tracking**: After successfully writing the output CSV, your Rust program must append a single line to `/home/user/experiments.txt` in the following exact format:
   `SUCCESS: Processed <N> rows.` (where `<N>` is the number of data rows processed, excluding the header).

**Execution:**
Build and run your Rust program so that the output file `/home/user/data/features.csv` and the log file `/home/user/experiments.txt` are generated.

Note: You can use any standard crates like `csv` and `serde`. Make sure to handle standard errors gracefully, but for this task, you can assume the input CSV is well-formed.