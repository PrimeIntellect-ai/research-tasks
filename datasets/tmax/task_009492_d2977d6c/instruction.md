You are an automation specialist tasked with building a high-performance data processing pipeline. 

A set of 10 binary sensor log files will be generated in `/home/user/sensor_data/`. Each file contains thousands of records. Each record is a 12-byte binary structure consisting of:
- `sensor_id`: a 32-bit signed integer (little-endian)
- `value`: a 64-bit float (IEEE 754 double precision, little-endian)

Your task is to build a multi-stage pipeline that processes this data in parallel, converts the aggregated results to CSV, and archives it to a simulated remote directory.

Step 1: Write a C++ program at `/home/user/aggregate.cpp` that:
- Takes exactly two command-line arguments: the input directory path and the output CSV file path.
- Finds all files with the `.bin` extension in the input directory.
- Reads and processes the files in **parallel** (you must use C++ `<thread>`, `<future>`, or similar parallel execution mechanisms). 
- Calculates the total sum of `value` for each unique `sensor_id` across all files.
- Writes the aggregated results to the specified output CSV file. The CSV must have a header `id,total_value` and be sorted by `id` in ascending order. The `total_value` should be printed with 2 decimal places of precision.

Step 2: Write a bash orchestration script at `/home/user/pipeline.sh` that:
- Compiles the C++ program using `g++` (output executable should be `/home/user/aggregator`). Ensure you link necessary threading libraries.
- Runs the executable, reading from `/home/user/sensor_data/` and writing to `/home/user/aggregated_results.csv`.
- Compresses the resulting CSV into a tarball at `/home/user/remote_sync/results.tar.gz` (this simulates transferring the file to a remote archive location).

Ensure `/home/user/pipeline.sh` is executable. You can assume standard C++17 capabilities.