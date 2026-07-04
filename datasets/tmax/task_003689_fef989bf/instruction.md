You are a data analyst tasked with processing a batch of IoT sensor data. Your goal is to build a lightweight Python data processing pipeline that reads CSV files, calculates summary statistics, detects anomalous readings, exports the anomalies to a SQLite database, and logs the pipeline's execution.

Data Location: 
The raw data is located in `/home/user/sensor_data/`. The directory contains multiple CSV files. Each CSV file has the following columns: `timestamp`, `sensor_id`, `temperature`.

Your script must be saved as `/home/user/process_sensors.py` and perform the following operations:

1. Data Ingestion & Aggregation:
Read all CSV files in `/home/user/sensor_data/`. Group the data by `sensor_id` and calculate the mean and population standard deviation (ddof=0) for the `temperature` readings across all files for each sensor.

2. Anomaly Detection:
Anomalies are defined as temperature readings that deviate by more than 2 standard deviations from the mean of that specific sensor (i.e., |temperature - mean| > 2 * std_dev). 
For each anomalous reading, calculate its Z-score: `(temperature - mean) / std_dev`.

3. Database Export:
Create a SQLite database at `/home/user/anomalies.db`.
Create a table named `temperature_anomalies` with the following columns: 
`timestamp` (TEXT), `sensor_id` (TEXT), `temperature` (REAL), and `z_score` (REAL).
Insert all detected anomalies into this table. Round the `z_score` to 2 decimal places.

4. Pipeline Logging:
Your script must log its progress to a file at `/home/user/pipeline.log`.
The log format should strictly follow this structure: `[YYYY-MM-DD HH:MM:SS] - [STEP] - [MESSAGE]`
You must include at least these three steps in your logs:
- `[STEP]: INGESTION`, `[MESSAGE]: Processed <X> rows` (where <X> is the total number of rows read).
- `[STEP]: ANOMALY_DETECTION`, `[MESSAGE]: Found <Y> anomalies` (where <Y> is the total number of anomalies).
- `[STEP]: EXPORT`, `[MESSAGE]: Successfully exported to SQLite`

Execute your script so the database and log files are generated.