You are an automation specialist creating a robust data workflow. 

We have a daily sensor log file located at `/home/user/raw_sensors.csv`. Standard shell tools like `awk` and `grep` are failing on this file because the `description` column contains embedded newlines inside double-quoted fields, which breaks standard line-by-line processing.

Your task is to write a C++ program that safely parses this CSV, processes the data, and outputs a clean dataset. 

Write your C++ code in `/home/user/process_data.cpp` and compile it to `/home/user/process_data`. Then execute it to produce the final output at `/home/user/processed_sensors.csv`.

**Input Format (`/home/user/raw_sensors.csv`):**
The CSV has a header: `id,timestamp,sensor_id,value,description`
- `id`: integer
- `timestamp`: ISO8601 format (`YYYY-MM-DDTHH:MM:SS`)
- `sensor_id`: string
- `value`: float
- `description`: string, enclosed in double quotes (`" "`), which may contain embedded newlines.

**Processing Requirements:**
1. **Data Sampling (Filtering):** Extract *only* the rows where `sensor_id` is exactly `TEMP_A`. Ignore all other sensors.
2. **Feature Extraction:** Keep only the `timestamp` and `value` fields for the output.
3. **Timestamp Alignment:** Parse the `timestamp` and align (round down) the time to the nearest minute. For example, `2023-10-12T14:35:59` must become `2023-10-12T14:35:00`.
4. **Normalization:** Normalize the `value` field using Min-Max scaling to a `[0.0, 1.0]` range. Assume the theoretical minimum possible value is `-50.0` and the maximum is `150.0`. 
   Formula: `normalized_value = (value - (-50.0)) / (150.0 - (-50.0))`
   Clamp the output to `[0.0, 1.0]` if any anomalous value exceeds this theoretical range.

**Output Format (`/home/user/processed_sensors.csv`):**
Create a headerless CSV with exactly two columns: `aligned_timestamp,normalized_value`.
Format the normalized value to exactly 4 decimal places (e.g., `0.3550`).

**Constraints:**
- Use standard C++17 only (no external libraries like Boost).
- Compile with `g++ -std=c++17 /home/user/process_data.cpp -o /home/user/process_data`.
- Properly handle RFC 4180 style embedded newlines in the double-quoted `description` column.