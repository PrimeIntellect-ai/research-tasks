You are a data analyst tasked with processing messy, multi-source time-series sensor data. 

You have been given two CSV files from different international manufacturing plants. Due to legacy system differences, they have different character encodings and contain messy data (duplicates, blank lines). 

Your goal is to clean the data, bucket the timestamps by hour, and compute the absolute difference in the hourly average values between the two sensors.

**Input Files:**
1. `/home/user/data/sensor_a.csv`: Contains data for Sensor A. Encoded in `UTF-16LE`.
2. `/home/user/data/sensor_b.csv`: Contains data for Sensor B. Encoded in `ISO-8859-1`.

Both files have the following columns (without a header row):
`timestamp,value,sensor_id`
Example row: `2023-10-01T10:15:30Z,45.5,A`

**Requirements:**
1. **Data Cleaning & Normalization**: 
   - Convert both files to standard UTF-8.
   - Remove any completely blank lines.
   - Remove duplicate rows (if a file has multiple identical rows, keep only one).
2. **Time-Based Bucketing**:
   - Truncate the timestamps to the start of the hour (e.g., `2023-10-01T10:15:30Z` becomes `2023-10-01T10:00:00Z`).
3. **Aggregation**:
   - Calculate the average `value` for Sensor A for each hour.
   - Calculate the average `value` for Sensor B for each hour.
4. **Distance Computation**:
   - For every hour where *both* Sensor A and Sensor B have data, compute the absolute difference between their average values. (Difference = |Avg_A - Avg_B|). Round the result to 1 decimal place.
5. **Output**:
   - Write the final results to `/home/user/output/hourly_distance.csv`.
   - The output must include a header: `hour,distance`
   - The rows should be sorted chronologically by hour.
   - Example output row: `2023-10-01T10:00:00Z,20.0`

Create the necessary output directories if they do not exist. You may use any combination of shell utilities (awk, sed, iconv, etc.) or write a script in Python/Ruby to accomplish this task.