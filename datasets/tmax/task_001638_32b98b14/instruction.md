You are a data analyst tasked with cleaning and processing a stream of IoT sensor data. 

I have a raw dataset located at `/home/user/sensors_raw.csv` containing IoT sensor readings. The file has the following columns:
`Timestamp,SensorID,CoordX,CoordY,Temperature`

Your goal is to process this dataset and produce a clean, analyzed output file at `/home/user/sensors_processed.csv`. 
You may write a script in any language you prefer to accomplish this, but ensure you only rely on standard libraries or install any dependencies you need.

Here are the exact processing steps you must implement:

1. **Hash-based Deduplication**: 
   Often, sensors double-post identical readings due to network retries. Deduplicate the records by keeping only the *first* occurrence (chronologically by `Timestamp`) of a reading. Two readings are considered duplicates if they have the exact same `SensorID,CoordX,CoordY,Temperature`. (You can use a hash of these four fields to identify duplicates).

2. **Distance Computation**:
   For each deduplicated record, calculate the Euclidean distance of the sensor from the origin (0,0) using `CoordX` and `CoordY`. Round the result to 2 decimal places.

3. **Windowed Rolling Aggregation**:
   For each `SensorID`, compute the rolling average of the `Temperature` based on up to the 3 *strictly previous* readings (chronologically) for that sensor. Do not include the current reading in its own previous rolling average. 
   - If there are no previous readings, the rolling average should be represented by the string `N/A`.
   - Otherwise, compute the mean of the 1, 2, or 3 previous temperatures and round it to 2 decimal places.

4. **Anomaly Detection**:
   Determine if the current reading is an anomaly. 
   - A reading is flagged as `ANOMALY` if a previous rolling average exists (not `N/A`) and the current `Temperature` is strictly greater than `1.5 * Rolling Average`. 
   - Otherwise, the status is `NORMAL`.

5. **Final Output Formatting**:
   Write the processed data to `/home/user/sensors_processed.csv` with the following columns:
   `Timestamp,SensorID,Distance,RollingAvgTemp,Status`
   Ensure the final CSV is sorted first by `Timestamp` (ascending as integers), and then by `SensorID` (ascending lexicographically).

Please write and execute the code to generate the final processed CSV file.