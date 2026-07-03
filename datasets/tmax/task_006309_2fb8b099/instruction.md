You are a data engineer tasked with building a lightweight ETL pipeline to process incoming telemetry data. 

We have a raw data file located at `/home/user/sensor_data.csv`. It contains three columns: `timestamp` (integer UNIX epoch), `sensor_id` (string), and `value` (float). 

Your objective is to write and execute a Python script at `/home/user/etl_pipeline.py` that performs the following steps:

1. **Logging Setup**: Configure logging to write to `/home/user/pipeline.log`. The log format must be exactly `%(asctime)s - %(levelname)s - %(message)s` (e.g., `2023-10-25 10:00:00,000 - INFO - Pipeline started`).
   - Log `Pipeline started` at the beginning.
   - Log `Processed <N> rows` after data transformation (where <N> is the total number of rows).
   - Log `Pipeline finished` at the end.

2. **Data Transformation (Rolling Statistics & Grouping)**: 
   - Read `/home/user/sensor_data.csv`.
   - Sort the data chronologically by `timestamp`.
   - Group the data by `sensor_id`.
   - Compute a 5-period rolling mean (`rolling_mean`) and a 5-period rolling standard deviation (`rolling_std`) on the `value` column for each sensor.
   - The first 4 rows of each group will naturally have `NaN` for these rolling metrics; leave them as missing/null values.

3. **Database Bulk Import**:
   - Save the transformed data (now with 5 columns: `timestamp`, `sensor_id`, `value`, `rolling_mean`, `rolling_std`) into a new SQLite database at `/home/user/metrics.db`.
   - The data must be stored in a table named `rolling_metrics`. 
   - Use an efficient bulk insertion method (like Pandas' `to_sql` or dumping to an intermediate CSV and using SQLite's `.import` command).

Write the script and execute it so that `/home/user/metrics.db` and `/home/user/pipeline.log` are successfully populated.