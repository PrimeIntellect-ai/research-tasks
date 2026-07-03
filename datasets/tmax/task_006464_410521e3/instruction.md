You are a data engineer dealing with a messy sensor dataset. A scheduled ETL job failed midway and retried multiple times, appending duplicate and overlapping records into a raw data file. 

Your task is to write a C++ program that cleans this data, processes it in parallel, aligns the time-series, and computes a similarity metric.

Here are the requirements for your C++ program (`/home/user/etl_processor.cpp`):

1. **Read Input**: Read a CSV file located at `/home/user/raw_sensor_data.csv`. The file has no header and contains rows in the format: `timestamp,sensor_id,value`
   - `timestamp` is an integer (Unix epoch).
   - `sensor_id` is a string (either `S1` or `S2`).
   - `value` is a floating-point number.

2. **Deduplication**: Due to the ETL retry bug, there are duplicate entries for the same `timestamp` and `sensor_id`. When duplicates exist, keep only the record with the **maximum** `value` for that `(timestamp, sensor_id)` pair.

3. **Resampling and Gap-Filling**: 
   - Determine the global minimum timestamp (`T_MIN`) and maximum timestamp (`T_MAX`) across all data (both sensors) after reading.
   - For each sensor, generate a continuous time-series from `T_MIN` to `T_MAX` at exactly **1-second intervals** (inclusive).
   - If a sensor is missing a value at a specific second, estimate it using **linear interpolation** between the nearest preceding and nearest succeeding timestamps. 
   - If a sensor lacks data before its first timestamp or after its last timestamp, carry forward the first/last available value to fill up to `T_MIN` / `T_MAX` (Zero-Order Hold for the edges).

4. **Parallel Processing**: The resampling and gap-filling for `S1` and `S2` must be executed in parallel using C++ threads (`std::thread`, `std::async`, or OpenMP).

5. **Distance Computation**: Once both time-series are aligned and gap-filled, compute the Euclidean distance between the `S1` series and the `S2` series across the `[T_MIN, T_MAX]` interval.

6. **Output**:
   - Write the aligned and resampled data to `/home/user/resampled.csv` with a header. Format: `timestamp,S1_value,S2_value`. Print values to exactly 4 decimal places.
   - Write the computed Euclidean distance to a file `/home/user/distance.txt`. Print the value to exactly 4 decimal places.

Compile your program using standard tools (e.g., `g++ -std=c++17 -pthread /home/user/etl_processor.cpp -o /home/user/etl_processor`) and execute it.