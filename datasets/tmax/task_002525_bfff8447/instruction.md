You are an automation specialist creating data processing workflows for an IoT edge network. 

You have been given three raw sensor data files from different edge devices. They contain unaligned timestamp data in "long" format. Your task is to write a C program that reads these files, performs time-based bucketing, aligns the timestamps, calculates the average value per bucket for each sensor, and merges them into a single "wide" format CSV file.

**Environment setup:**
The input files are located at:
- `/home/user/data/sensor_A.csv`
- `/home/user/data/sensor_B.csv`
- `/home/user/data/sensor_C.csv`

Each file has the following format:
```
timestamp,value
1622548810,23.5
1622548825,23.8
...
```
`timestamp` is an integer UNIX epoch time. `value` is a float. The files do not have headers, just the raw data rows.

**Your Objective:**
Write a C program at `/home/user/process_sensors.c` that does the following:

1. **Time-Based Bucketing & Timestamp Alignment:** 
   Group the data points from all three sensors into 60-second intervals. The bucket timestamp is calculated as `(timestamp / 60) * 60` (integer division).
   
2. **Aggregation:**
   If a sensor has multiple readings in the same 60-second bucket, calculate the arithmetic mean (average) of those values.

3. **Joins & Reshaping (Long to Wide):**
   Combine the aggregated data from all three sensors into a single wide-format output. If any sensor has data for a specific bucket, that bucket must appear in the output. If a sensor does *not* have data for a bucket, use `-999.00` as the placeholder value for that sensor.

4. **Output Specifications:**
   - The output must be written to `/home/user/output/merged_sensors.csv`.
   - The output must include a header: `bucket_timestamp,avg_A,avg_B,avg_C`.
   - The rows must be sorted in ascending order by `bucket_timestamp`.
   - All float values (averages and placeholders) must be printed to exactly 2 decimal places (e.g., `23.50`, `-999.00`).

**Action Items:**
1. Ensure the directories exist (`/home/user/data` and `/home/user/output`). Assume the input data is already populated.
2. Write the C code to `/home/user/process_sensors.c`.
3. Compile the code (e.g., using `gcc`).
4. Execute the compiled program to generate the required output file.