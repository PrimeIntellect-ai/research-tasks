You are a data scientist tasked with cleaning a corrupted time-series dataset from IoT temperature sensors.

The input data is located at `/home/user/data/raw_sensors.jsonl`. This file contains JSON-Lines data, but a logging bug caused some location metadata to contain malformed unicode escape sequences (e.g., `\uXXth` instead of valid hex). Standard JSON parsers will fail to read these lines. 

Your goal is to write a Go program (in `/home/user/workspace/process.go`) that does the following:
1. **Handle the Corruption:** Read the JSONL file and safely bypass or strip the malformed unicode escape sequences so the lines can be parsed.
2. **Sort and Group:** Group the records by `sensor_id` and sort them chronologically by `timestamp`.
3. **Resample and Gap-Fill:** The data spans the day of `2023-10-01`. Create 24 hourly buckets for each sensor (`00:00:00` to `23:00:00`). 
   - A bucket's value is the average of all temperature readings (`temp`) that occurred within that hour (e.g., the `02:00:00` bucket averages all readings from `02:00:00` up to `02:59:59`).
   - **Gap-filling:** If a bucket has no readings, forward-fill the value from the previous hour's bucket. If the very first bucket (`00:00:00`) has no readings and no previous data, default its value to `0.0`.
4. **Summary Statistics:** For each sensor, calculate the mean, maximum, and minimum temperatures across the **24 resampled hourly buckets**.
5. **Output:** Write the results to `/home/user/data/summary.csv` with the following header: `sensor_id,mean_temp,max_temp,min_temp`.
   - Sort the output CSV alphabetically by `sensor_id`.
   - Format all floating-point numbers to exactly 2 decimal places (e.g., `14.27`).

Requirements:
- You must use Go to process the data.
- Do not modify the original `/home/user/data/raw_sensors.jsonl` file.
- The output must exactly match the requested CSV format.