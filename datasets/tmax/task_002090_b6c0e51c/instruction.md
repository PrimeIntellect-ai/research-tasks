You are a data analyst troubleshooting a buggy ETL pipeline that produces duplicate records and out-of-order data during retries. You need to write a C++ program to clean the data and detect anomalies.

The input data is located at `/home/user/sensor_data.csv` with the header: `timestamp,sensor_id,value`.
- `timestamp` is an integer.
- `sensor_id` is a string that may contain leading/trailing spaces and mixed casing.
- `value` is a float.

Write a C++ program (e.g., in `/home/user/process.cpp`) that reads this CSV and performs the following:

1. **Normalization**: For each row, strip leading and trailing whitespace from the `sensor_id` and convert it to uppercase.
2. **Validation**: Drop any rows where `value` cannot be parsed as a float, or where `value` is strictly less than 0.
3. **Deduplication / Sequencing**: For each normalized `sensor_id`, process records in the order they appear in the file. Only accept a record if its `timestamp` is strictly greater than the `timestamp` of the last *accepted* record for that specific `sensor_id`. (This naturally drops exact duplicates and out-of-order retry artifacts).
4. **Rolling Aggregation & Anomaly Detection**:
   - For each accepted record, calculate the rolling average of the *up to 3 most recent previously accepted values* for that sensor (do not include the current record's value in its own average calculation).
   - If there are no previous accepted records for the sensor, no average can be calculated and it is not an anomaly.
   - An anomaly is detected if the current `value` is strictly greater than `2.0 * rolling_avg`.
   - Update the rolling window with the current value after checking for an anomaly.

Output the anomalies to `/home/user/anomalies.csv` with the following format:
`timestamp,sensor_id,value,rolling_avg`

Format both `value` and `rolling_avg` to exactly 2 decimal places. Include the header row.

Compile and run your C++ program to generate the output file.