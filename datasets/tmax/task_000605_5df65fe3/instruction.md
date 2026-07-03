You are a data scientist responsible for cleaning and engineering features from a large IoT time-series dataset. You need to build a highly optimized Bash-driven ETL pipeline that processes raw sensor data, extracts features using windowed aggregations, bulk loads the data into a database, and caches the latest state in a key-value store.

System Environment & Services:
We are using a multi-service architecture with PostgreSQL and Redis. 
1. First, start the local services by running the provided script: `bash /app/start_services.sh`. This will start PostgreSQL (port 5432, user: `postgres`, db: `sensor_db`) and Redis (port 6379).

Data Source:
A raw CSV file is located at `/home/user/data/sensors.csv`. It contains 500,000 rows.
Format: `ts,sensor_id,value` (no header).
- `ts`: Integer Unix timestamp.
- `sensor_id`: String identifier (e.g., "s1", "s2").
- `value`: Numeric float.

Your Objectives:
Write a single, highly efficient Bash script at `/home/user/process.sh` that performs the following steps when executed:

1. **Database Initialization**: Connect to PostgreSQL (`sensor_db`) and create two tables:
   - `raw_data`: columns `ts` (BIGINT), `sensor_id` (VARCHAR), `value` (NUMERIC).
   - `sensor_features`: columns `ts` (BIGINT), `sensor_id` (VARCHAR), `rolling_avg` (NUMERIC).

2. **Bulk Import**: Efficiently bulk load all records from `/home/user/data/sensors.csv` into the `raw_data` table.

3. **Feature Extraction (Windowed Aggregation)**: Calculate a 5-period rolling average of the `value` column for each `sensor_id`, ordered strictly by `ts` ascending. The rolling window should include the current row and up to 4 preceding rows for that specific sensor. Insert these results into the `sensor_features` table.

4. **Cache the Latest State**: For each `sensor_id`, find the most recent `rolling_avg` (the one with the highest `ts`). Export these latest values and bulk update Redis. The Redis keys should be formatted as `sensor:<sensor_id>` and the value must be the `rolling_avg` (rounded to 2 decimal places).

Performance Constraint:
The script `/home/user/process.sh` will be evaluated on its execution speed. To pass, the entire end-to-end process (table creation, bulk load, windowed aggregation, and Redis caching) must complete in **under 10.0 seconds** for the 500,000-row dataset. 

Ensure your script is executable (`chmod +x /home/user/process.sh`) and handles all database and cache interactions silently or with minimal stdout output to avoid I/O bottlenecks.