You are a data analyst tasked with processing a batch of sensor data. You have been given a raw CSV file at `/home/user/raw_sensors.csv` containing temperature readings from three different rooms. 

The file is in a "wide" format with the following columns:
`timestamp,room_A,room_B,room_C`

However, the data has several issues:
1. **Duplicates**: Due to a logging error, there are exact duplicate rows in the file. You must implement a hash-based deduplication step (e.g., computing a hash of the row or using standard deduplication that relies on hashing under the hood) to keep only the first occurrence of each unique row.
2. **Missing Time Steps**: The sensors are supposed to record data every exactly 1 hour, but some hourly timestamps are missing.
3. **Format**: The downstream mathematical modeling tools require the data in a "long" format rather than a "wide" format.

Write a Python script to process this data. Your script must:
1. Read `/home/user/raw_sensors.csv`.
2. Remove completely identical duplicate rows.
3. Parse the `timestamp` column as datetimes and sort the data chronologically.
4. Resample the time series to a strict 1-hour frequency (`1H`). For any newly created timestamps (the gaps), fill the missing temperature values using forward-fill (carrying the last known observation forward).
5. Reshape the dataset from wide format to long format. The resulting columns must be exactly `timestamp`, `room`, and `temperature`.
6. Sort the final dataset primarily by `timestamp` (ascending) and secondarily by `room` (alphabetical).
7. Save the processed data to `/home/user/processed_sensors.csv` (including headers, timestamp formatted as `YYYY-MM-DD HH:MM:SS`).

Ensure your Python script executes successfully and produces the required output file.