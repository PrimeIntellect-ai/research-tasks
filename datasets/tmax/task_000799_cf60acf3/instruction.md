You are an automation specialist building a scalable data pipeline for an IoT sensor network. 

Raw time-series data is periodically dumped into `/home/user/raw_sensors/` as wide-format CSV files. You need to create a multi-language workflow to reshape, stratify, sample, and aggregate this data. 

Here are your requirements:

1. **Wide-to-Long Reshaping & Stratified Sampling (Python)**
   Write a Python script `/home/user/scripts/process_sensor.py` that takes an input CSV file path and an output CSV file path as arguments.
   The input CSVs have the header: `timestamp, s1_temp, s1_vib, s2_temp, s2_vib`.
   - **Reshape**: Convert this wide format into a long format with columns: `timestamp, sensor, metric, value`. 
     (e.g., a column `s1_temp` becomes `sensor`="s1", `metric`="temp").
   - **Stratified Sampling**: Group the reshaped data by `metric`. For each `metric` stratum, sort the rows strictly by `timestamp` in ascending order. Keep only the earliest 50% of the rows for each metric (use ceiling division if the number of rows is odd: `math.ceil(N / 2)`).
   - Write the filtered long-format data to the specified output CSV path. It must include the header: `timestamp,sensor,metric,value`.

2. **Parallel Orchestration (Bash)**
   Write a Bash script `/home/user/scripts/run_pipeline.sh` that:
   - Creates the output directory `/home/user/processed/` if it doesn't exist.
   - Finds all `.csv` files in `/home/user/raw_sensors/`.
   - Uses a parallel processing tool (like `xargs -P` or GNU `parallel`) to run `process_sensor.py` on all input files simultaneously.
   - Saves the processed files in `/home/user/processed/` keeping their original filenames.

3. **Aggregation (Any scripting language e.g. awk, ruby, perl, or python)**
   Write a script `/home/user/scripts/aggregate.py` (or `.sh`, `.awk`, etc.) that reads ALL the processed long-format CSVs in `/home/user/processed/` and calculates the global average `value` for each `metric`.
   - Output these averages as a JSON object to `/home/user/summary.json`. 
   - Keys must be the `metric` names (e.g., `"temp"`, `"vib"`), and values must be the averages rounded to exactly 2 decimal places (e.g., `{"temp": 24.51, "vib": 0.15}`).

**Setup Note:** You must create the `/home/user/scripts/` directory. Assume the raw data is already present in `/home/user/raw_sensors/` before you run your workflow. Do not modify the raw data files. Execute your workflow and ensure `/home/user/summary.json` is generated successfully.