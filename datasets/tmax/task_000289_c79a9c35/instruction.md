You are an investigative log analyst trying to identify coordinated bot behavior based on API latency patterns. You have been given a raw log file of API requests, but the data is noisy, incomplete, and across different baseline network speeds.

Your task is to write a Python script `/home/user/analyze_logs.py` to process the logs, normalize the data, and find the two IP addresses that have the most similar latency profiles over a specific time window. 

The raw data is located at `/home/user/api_latency.csv` with columns: `timestamp,ip,latency_ms`.

Your script must perform the following pipeline:

1. **Quality Gate (Validation Checkpoint):**
   - Read the CSV. 
   - Discard any `ip` that has strictly fewer than 5 raw log entries in the entire dataset.

2. **Resampling & Gap-Filling:**
   - For each valid IP, aggregate the data into exactly 10 one-minute bins starting from `2023-10-01T10:00:00` up to `2023-10-01T10:09:59` (i.e., bin 0 is 10:00:00-10:00:59, bin 9 is 10:09:00-10:09:59).
   - The value for each bin should be the mean `latency_ms` of all requests in that minute.
   - **Gap-filling:** If an IP has no logs in a specific minute, forward-fill the value from the previous minute. If the first minute(s) (e.g., bin 0) are empty, back-fill using the first available value for that IP.

3. **Normalization:**
   - Standardize the 10-bin time series for each IP using Z-score normalization: `(value - mean) / standard_deviation`.
   - Use the sample standard deviation (N-1 degrees of freedom). If the standard deviation is 0 (all values are identical), set all normalized values for that IP to `0.0`.

4. **Similarity Computation:**
   - Calculate the Euclidean distance between the normalized 10-bin time series of all pairs of valid IPs.
   - Identify the pair of IPs with the smallest Euclidean distance (most similar latency profile).

5. **Output:**
   - Save the result to `/home/user/closest_ips.json` with exactly this structure:
     ```json
     {
       "ip1": "<lexicographically_smaller_ip>",
       "ip2": "<lexicographically_larger_ip>",
       "distance": <euclidean_distance_rounded_to_4_decimal_places>
     }
     ```

Run your script to produce the output file.