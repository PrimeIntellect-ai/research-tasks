You are an ML engineer preparing a training dataset. You need to build a high-performance C++ data pipeline that joins raw sensor readings with their respective calibration profiles, computes the corrected values, and benchmarks the inference/processing performance.

Here are your requirements:

1. **Input Data**:
   - Raw data is located at `/home/user/raw_sensors.csv`. Format: `timestamp,sensor_id,raw_value`
   - Calibration profiles are at `/home/user/calibrations.json`. It is a simple JSON object mapping `sensor_id` to their calibration parameters: `{"sensor_id": {"scale": float, "offset": float}}`

2. **Processing Logic**:
   - Write a C++ program named `/home/user/process_data.cpp`.
   - The program must load the calibrations and stream through the CSV.
   - For each row, calculate the corrected value using the formula: `corrected_value = (raw_value * scale) + offset`
   - You must use double-precision floating-point numbers (`double`) for all calculations to ensure numerical accuracy.
   - If a `sensor_id` from the CSV is missing in the JSON, drop that row (do not output it).

3. **Outputs**:
   - **Data Output**: The program must write the corrected data to `/home/user/processed.csv`.
     - Format: `timestamp,sensor_id,corrected_value`
     - The `corrected_value` MUST be formatted to exactly 4 decimal places (e.g., `12.1000`).
     - Include a header: `timestamp,sensor_id,corrected_value`
   - **Benchmarking Output**: The program must track the total number of valid records processed and write a summary to `/home/user/metrics.txt` containing exactly this text format:
     ```
     Total valid records: <NUMBER>
     ```

4. **Implementation Constraints**:
   - Write, compile, and execute the C++ code entirely within your environment.
   - You may download third-party single-header C++ libraries (like `nlohmann/json.hpp` via `wget`) to `/home/user/` to help parse the JSON, as you do not have root access to install global packages.
   - Compile your program using `g++ -O3 -std=c++17 process_data.cpp -o process_data`.