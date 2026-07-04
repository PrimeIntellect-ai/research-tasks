You are an ETL data engineer. We have received a batch of raw sensor telemetry data from our industrial IoT system, and we need a highly efficient C++ pipeline to process it. 

The raw data is located at `/home/user/raw_telemetry.csv`. It is a headerless CSV file with the following columns:
1. `sensor_id` (string)
2. `timestamp` (long integer)
3. `temperature` (double)

You need to write a C++ program at `/home/user/etl_processor.cpp` that performs Data Validation, Grouping, Sorting, and Aggregation.

### Validation Constraints
Your program must read the CSV and strictly ignore any rows that violate the following constraints:
- `sensor_id` must begin exactly with the prefix `SN-`.
- `timestamp` must be strictly greater than `0`.
- `temperature` must be between `-50.0` and `150.0` (inclusive).

### Aggregation & Sorting
For all valid rows, group the records by `sensor_id`. For each distinct `sensor_id`, calculate:
- `count`: the number of valid records
- `min_temp`: the minimum temperature recorded
- `max_temp`: the maximum temperature recorded
- `avg_temp`: the mean temperature

### Output
Your C++ program should write the aggregated results to `/home/user/summary_stats.csv`.
- The output must include a header: `sensor_id,count,min_temp,max_temp,avg_temp`
- The output rows must be sorted lexicographically by `sensor_id` in ascending order.
- The floating-point values (`min_temp`, `max_temp`, `avg_temp`) must be printed to exactly 2 decimal places.

### Execution
1. Write your code in `/home/user/etl_processor.cpp`.
2. Compile it using standard `g++` (e.g., `g++ -O3 -std=c++17 -o /home/user/etl_processor /home/user/etl_processor.cpp`).
3. Run the compiled executable so that it generates `/home/user/summary_stats.csv`.

Ensure your C++ code is robust and handles standard file I/O properly. Do not use external C++ libraries (like Boost); rely only on the standard library (`<iostream>`, `<fstream>`, `<sstream>`, `<string>`, `<vector>`, `<map>`, `<iomanip>`, etc.).