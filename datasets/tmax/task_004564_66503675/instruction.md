You are an automation specialist building a data processing pipeline for a fleet of IoT weather stations. You need to process noisy sensor data, handle missing values, smooth the data, and extract a stratified sample for reporting.

You must write a Go program located at `/home/user/process_sensors.go` that performs the following workflow:

1. **Multi-format Reading:**
   - Read device metadata from `/home/user/devices.json`. This is a JSON array of objects with keys: `device_id` (string), `region` (string), and `active` (boolean).
   - Read raw sensor data from `/home/user/sensor_data.csv`. This CSV has no header. The columns are: `timestamp` (integer, Unix epoch), `device_id` (string), `temperature` (string/float), and `humidity` (string/float).
   - Filter out and ignore any records from devices where `active` is `false` or the device is not present in `devices.json`.

2. **Interpolation and Imputation:**
   - Group the sensor data by `device_id` and sort each group chronologically by `timestamp`.
   - The `temperature` column may contain empty strings (`""`), indicating a missing reading.
   - For each active device, fill in missing temperature values using **linear interpolation** based on the `timestamp`. 
   - *Formula:* `T_missing = T_prev + (T_next - T_prev) * (t_missing - t_prev) / (t_next - t_prev)`.
   - You can assume that for any given device, the very first and very last chronological records will always have a valid temperature.

3. **Rolling Statistics Computation:**
   - For each device, compute a 3-point Simple Moving Average (SMA) of the *interpolated* temperatures to smooth out noise.
   - The smoothed temperature at index `i` is the average of the temperatures at `i-2`, `i-1`, and `i`.
   - For the first two points of a device's series (where a full window of 3 is not available), compute the average of the available points up to that index (e.g., `SMA_0 = T_0`, `SMA_1 = (T_0 + T_1)/2`).

4. **Data Sampling and Stratification:**
   - Combine all the processed records from all active devices.
   - Stratify the records by `region`.
   - For each region, sample exactly the **top 2 records** with the highest `smoothed_temp`.
   - Resolve any exact ties in `smoothed_temp` by selecting the record with the older (smaller) `timestamp` first, then alphabetically by `device_id`.

5. **Output:**
   - Write the final stratified sample to `/home/user/top_sensors.json`.
   - The output must be a JSON array of objects, formatted strictly like this:
     ```json
     [
       {"region": "East", "device_id": "D2", "timestamp": 1620000120, "smoothed_temp": 28.5},
       ...
     ]
     ```
   - The array must be sorted alphabetically by `region` (ascending), and within each region, descending by `smoothed_temp`. `smoothed_temp` must be rounded to exactly 2 decimal places if necessary, or simply represented as a standard float.

Compile and run your Go program to produce the final JSON file. You may use standard Go library packages only.