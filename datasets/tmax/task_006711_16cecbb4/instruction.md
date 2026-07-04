You are a data scientist working on cleaning a set of sensor telemetry data. You need to write a C++ pipeline to parse, join, and aggregate datasets. 

There are two input files:
1. `/home/user/measurements.csv`: A CSV file containing sensor readings. 
   - Columns: `timestamp,sensor_id,value,notes`
   - `timestamp`: Integer (UNIX epoch).
   - `sensor_id`: Integer.
   - `value`: Floating point number.
   - `notes`: A string enclosed in double-quotes (`""`). *Warning*: This column frequently contains embedded newline characters (`\n`) within the quotes. A naive line-by-line reading will split these rows incorrectly and silently corrupt the data.
2. `/home/user/sensors.tsv`: A Tab-Separated Values (TSV) file containing sensor metadata.
   - Columns: `sensor_id\tstatus` (where status is either `active` or `inactive`).

Your task is to write a standard C++17 program at `/home/user/process.cpp` (using only the C++ Standard Library, no third-party libraries like Boost) that performs the following steps:
1. Reads and parses both files.
2. **Joins/Filters**: Discard any measurements from sensors that are marked as `inactive` in the TSV file.
3. **Sorts**: Order the remaining valid measurements primarily by `sensor_id` (ascending), and secondarily by `timestamp` (ascending).
4. **Aggregates (Rolling Statistics)**: For each active sensor, calculate the rolling average of the `value` column using a window of the last 3 readings (the current reading and up to 2 previous readings for that specific sensor).
5. Writes the result to `/home/user/output.csv` with exactly this header: `sensor_id,timestamp,rolling_avg`. The `rolling_avg` must be rounded to exactly two decimal places (e.g., `12.50`).

Compile your program using `g++ -std=c++17 -O2 /home/user/process.cpp -o /home/user/process`, run it, and ensure `/home/user/output.csv` is correctly generated.