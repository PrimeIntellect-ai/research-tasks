You are a data scientist cleaning a messy dataset of IoT sensor readings from a server room. You need to write a shell script `/home/user/process_data.sh` that transforms, cleans, and analyzes the dataset using standard command-line tools (like `awk`, `sed`, `grep`, `bash`). 

You have a raw CSV file located at `/home/user/raw_sensors.csv` containing wide-format data. 
The columns are: `Timestamp,R1_Temp,R1_Hum,R2_Temp,R2_Hum`

Your script must perform the following pipeline and output the result to `/home/user/processed_sensors.csv`:

1. **Wide-to-Long Reshaping:** 
   Convert the dataset from wide format into a long format. The new columns must be exactly: `Timestamp,RackID,Metric,Value`

2. **Regex Standardization:**
   During the reshape, extract the Rack ID and Metric from the column headers using regex patterns.
   - Standardize `R1` and `R2` to `Rack1` and `Rack2`.
   - Standardize `Temp` to `Temperature` and `Hum` to `Humidity`.
   (e.g., `1000,22.0` from the `R1_Temp` column becomes `1000,Rack1,Temperature,22.0`)

3. **Windowed Aggregation (Rolling Average):**
   For each unique `RackID` and `Metric` combination, sort the data chronologically by `Timestamp` (ascending). 
   Compute a rolling moving average of the `Value` over a window of the last 3 readings (including the current reading). 
   - If there are fewer than 3 readings available (i.e., the first and second rows of a group), compute the average using the available readings.
   - Format the moving average to exactly 2 decimal places.

4. **Distance Computation (Anomaly Detection):**
   Calculate the absolute difference (distance) between the current `Value` and the calculated `MovingAvg`.
   - Format this distance to exactly 2 decimal places.

The final CSV at `/home/user/processed_sensors.csv` must be comma-separated and contain a header. 
It must be sorted primarily by `RackID` (ascending), then by `Metric` (ascending), and finally by `Timestamp` (ascending). 
The columns must be:
`Timestamp,RackID,Metric,Value,MovingAvg,Distance`

Make sure your script `process_data.sh` is executable and run it to produce the output file.