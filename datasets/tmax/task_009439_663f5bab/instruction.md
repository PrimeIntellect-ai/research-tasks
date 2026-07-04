You are acting as a data analyst. You have been given a set of legacy sensor data files located in `/home/user/raw_data`. 

Your objective is to clean this data, load it into a database, and perform changepoint/anomaly detection to find failing sensors.

Here are the specific requirements:
1. **Character Encoding:** The CSV files in `/home/user/raw_data` were exported from an old Windows system and are encoded in UTF-16LE. You must convert these files to UTF-8.
2. **Database Import:** Create an SQLite database at `/home/user/sensor_data.db`. Create a table named `readings` with the schema: `timestamp TEXT`, `sensor_id TEXT`, `temperature REAL`. Bulk import the cleaned UTF-8 CSV data into this table. The CSV files contain a header row: `timestamp,sensor_id,temperature`.
3. **Anomaly Detection:** Write a Bash script at `/home/user/detect_anomalies.sh` that detects anomalous temperature jumps. An anomaly is defined as an absolute difference of strictly more than 15.0 degrees between a reading and the *immediately preceding* reading from the *same* `sensor_id` (ordered chronologically by `timestamp`). 
4. **Output:** Your script `detect_anomalies.sh` must execute the necessary queries/processing and output the detected anomalies to `/home/user/anomalies.csv`. 
    - The output file must be a standard comma-separated CSV.
    - It must include a header row exactly as: `sensor_id,timestamp,temperature,previous_temperature`.
    - The rows must be sorted by `timestamp` ascending, and then by `sensor_id` ascending.

Ensure the bash script is executable. You may use `sqlite3`, `awk`, `iconv`, and other standard Linux tools to accomplish this. Do not use root/sudo privileges.