You are a data engineer building a lightweight ETL pipeline in C to process IoT sensor telemetry data. 

We have a raw data file simulating a remote storage drop located at `/home/user/remote_server/raw_telemetry.csv`. 

Your task is to write a C program, compile it, run it to process the data, and transfer the output. 

Follow these steps exactly:
1. Create a working directory at `/home/user/workspace` and write a C program named `process_telemetry.c` inside it.
2. The C program must read a CSV file (passed as an argument or hardcoded to read the raw telemetry file).
3. The raw CSV contains no header. Each row has 5 columns: `timestamp,sensor_id,temperature,humidity,status`.
4. Implement constraint-based validation for each row. A row is ONLY valid if it meets ALL the following criteria:
   - `timestamp`: Must be a strictly positive integer (> 0).
   - `sensor_id`: Must be exactly 4 characters long, starting with the uppercase letter 'S' followed by exactly 3 digits (e.g., "S015").
   - `temperature`: Must be a floating-point number between -50.0 and 150.0 (inclusive).
   - `humidity`: Must be a floating-point number between 0.0 and 100.0 (inclusive).
   - `status`: Must be exactly the string "OK" or "WARN". Any other status (like "ERR", "FAIL", etc.) makes the row invalid.
5. If a row fails any validation, silently drop it.
6. For valid rows, perform a feature extraction transform: calculate the `heat_index`, defined as `temperature + (0.5 * humidity)`.
7. The C program should output the valid extracted features to a file named `processed.csv` in the current working directory. The format must be `timestamp,sensor_id,heat_index` where `heat_index` is formatted to exactly 2 decimal places.
8. Compile your C program using `gcc` and run it against the raw telemetry data.
9. Finally, simulate uploading the processed data back to the remote server by moving `processed.csv` to `/home/user/remote_server/archive/processed_telemetry.csv`.

Ensure your C code handles file I/O properly and avoids buffer overflows. You may use standard bash commands to compile, execute, and move files around.