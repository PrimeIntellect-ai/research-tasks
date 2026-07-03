You are an automation specialist tasked with fixing a broken sensor data pipeline. 

We have a daily CSV extract located at `/home/user/data/sensor_log.csv`. The previous pipeline was silently dropping rows because the `notes` column sometimes contains embedded newlines. Furthermore, the timestamps come from different regions and are in mixed formats with various timezone offsets.

Write a Python script at `/home/user/process_sensors.py` to process this data and load it into an SQLite database. You may use `pandas` (you can install it via `pip`).

Your script must perform the following:
1. **Robust CSV Parsing:** Read `/home/user/data/sensor_log.csv` correctly, ensuring rows with embedded newlines inside the quoted `notes` column are not dropped or corrupted.
2. **Timestamp Alignment:** Parse the `timestamp` column and convert all times to UTC. Format the output in the database as an ISO 8601 string: `YYYY-MM-DDTHH:MM:SSZ`.
3. **Anomaly Detection:** We need to flag sudden temperature spikes. Add a new boolean column (or integer 0/1) named `is_anomaly`. Sort the data chronologically for each `sensor_id`. A reading is an anomaly (`True` or `1`) if the absolute difference in `temperature` between it and the *immediately preceding* reading for that **same** `sensor_id` is strictly greater than 20.0. The first chronological reading for any sensor is never an anomaly.
4. **Database Bulk Export:** Save the transformed data into an SQLite database located at `/home/user/data/sensors.db` in a table named `readings`. The table should contain the columns: `sensor_id`, `timestamp`, `temperature`, `notes`, and `is_anomaly`.

Execute your script so the database is populated.