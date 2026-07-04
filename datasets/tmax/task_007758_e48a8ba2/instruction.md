You are an automation specialist building a fast data processing pipeline. We have a stream of sensor data that was saved into two different formats. 

Your task is to write a C++ program (`/home/user/process.cpp`) that reads from these two formats, computes a rolling average using parallel processing, and writes the output to a new file.

Input Files:
1. `/home/user/data.csv`: A CSV file containing sensor readings. 
   Format: `sensor_id` (int32), `timestamp` (int64), `value` (double).
   Example: `1,1620000000,45.5`
2. `/home/user/data.bin`: A binary file containing sensor readings in a packed, little-endian format.
   Format: struct of `sensor_id` (int32), `timestamp` (int64), `value` (double). (Total 20 bytes per record).

Processing Requirements:
1. Read all records from both `data.csv` and `data.bin`.
2. Group the records by `sensor_id`.
3. Utilize parallel data processing (e.g., C++ `std::thread`, `std::async`, or OpenMP) to process the sensors concurrently.
4. For each `sensor_id`, compute the rolling average of the `value` over a window of the **last 3 readings** (including the current reading). The readings must be ordered by `timestamp` ascending. 
   - If a sensor has only 1 reading so far, the average is just that reading.
   - If 2 readings, the average is the mean of those 2.
   - If 3 or more, the average is the mean of the current and the previous 2 readings.

Output Requirements:
1. Write the results to `/home/user/output.csv`.
2. The format must be: `sensor_id,timestamp,rolling_average`.
3. The `rolling_average` must be formatted to exactly 4 decimal places (e.g., `45.5000`).
4. The final output file must be strictly ordered by `timestamp` ascending. If multiple records have the same timestamp, order them by `sensor_id` ascending.

Compile and run your code. You can use standard C++17. For OpenMP, compile with `-fopenmp`. For standard threads, use `-pthread`. Produce the final `/home/user/output.csv` file.