You are a data analyst working on testing a new ETL and inference pipeline for environmental sensor data. 

I need you to write a Python script that processes a raw CSV file, transforms the data, and runs a simple scoring model to test numerical accuracy.

The raw data is located at `/home/user/sensor_data.csv` and contains the following columns: `timestamp`, `sensor_id`, `temperature`, `humidity`.

Your script must perform the following steps:
1. **ETL / Aggregation:** Group the data by `sensor_id`. For each sensor, calculate the mean `temperature` and the maximum `humidity`.
2. **Model Inference:** Calculate a `risk_score` for each sensor using the following simple linear model formula:
   `risk_score = (mean_temp * 1.5) + (max_humidity * 0.8) - 10.0`
3. **Output:** Save the results to a new CSV file at `/home/user/sensor_risk_report.csv`.
   - The output CSV must have exactly these columns in order: `sensor_id`, `mean_temp`, `max_humidity`, `risk_score`.
   - The rows must be sorted in ascending order by `sensor_id`.
   - All numerical values (`mean_temp`, `max_humidity`, `risk_score`) must be rounded to exactly 2 decimal places.
   - Include the header row.

Write and execute the Python script to produce the output file. You may use standard Python libraries, `pandas`, or `numpy`.