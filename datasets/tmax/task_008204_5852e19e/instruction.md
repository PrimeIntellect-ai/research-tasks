You are a data engineer tasked with building a robust, reproducible ETL (Extract, Transform, Load) pipeline in C++ to process raw IoT sensor data. 

There is a raw data file located at `/home/user/raw_data.csv` containing streaming sensor records. The file has no header. 

Your goal is to write a C++ program that enforces a strict data schema, filters out invalid or error records, calculates the average temperature for each sensor, and outputs a summarized CSV. Finally, you need to create a reproducible bash script to compile and run your pipeline.

### 1. Data Schema Enforcement
Each row in the CSV is expected to have exactly four comma-separated columns: `timestamp,sensor_id,temperature,status`.
You must enforce the following strict schema. If a row violates ANY of these rules, it must be completely discarded:
- `timestamp`: Must be a valid positive integer.
- `sensor_id`: Must be a string starting exactly with `"S-"` followed by one or more digits (e.g., `S-001`, `S-42`).
- `temperature`: Must be a valid floating-point number between `-50.0` and `50.0` inclusive.
- `status`: Must be exactly the string `"OK"` or `"ERR"`.

### 2. Data Transformation (ETL)
For all rows that pass the schema validation:
- You must ignore any rows where `status` is `"ERR"`.
- For the remaining rows (where `status` is `"OK"`), compute the average temperature for each unique `sensor_id`.

### 3. Output Format
Your program should write the aggregated results to `/home/user/summary.csv`.
- The output must contain two columns: `sensor_id,average_temperature`.
- The `average_temperature` must be formatted to exactly 2 decimal places.
- The rows must be sorted alphabetically by `sensor_id`.

### 4. Reproducible Pipeline
- Write your C++ code in `/home/user/etl_pipeline.cpp`.
- Create a bash script at `/home/user/run_pipeline.sh` that:
  1. Compiles `/home/user/etl_pipeline.cpp` into an executable named `/home/user/etl.out` using `g++` (use `-std=c++17`).
  2. Runs the executable to process `/home/user/raw_data.csv` and generate `/home/user/summary.csv`.
- Ensure `/home/user/run_pipeline.sh` is executable.

You must handle the file reading, schema validation, and CSV formatting entirely within your C++ code. Do not use external libraries (like Boost) outside the standard C++17 library.