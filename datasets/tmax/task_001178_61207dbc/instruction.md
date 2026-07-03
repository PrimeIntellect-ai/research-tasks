You are a data analyst tasked with building a resilient data processing pipeline and serving the results via an HTTP API. 

We have a set of legacy CSV files containing sensor readings in `/home/user/raw_data/`. Due to system glitches, these files have various issues:
1. `sensor_1.csv` contains embedded newlines in the "remarks" column.
2. `sensor_2.csv` was exported from a legacy Windows machine and is encoded in Windows-1252.
3. `sensor_metadata.csv` contains information about the sensors.

Your objectives:
1. **Data Cleaning & Integration**: Write a Python script to parse these files correctly. Merge the sensor readings with the `sensor_metadata.csv` on the `sensor_id` column.
2. **Resampling & Gap-Filling**: The sensors are supposed to report every 5 minutes, but some readings are missing. Group the joined data by `sensor_id` and resample the time series to regular 5-minute intervals (aligned to the hour, e.g., 10:00, 10:05). For any missing intervals, forward-fill the `temperature` and `humidity` values (up to a limit of 3 consecutive missing intervals).
3. **Data Validation/Hashing**: We have a legacy stripped binary located at `/app/data_signer`. For each valid (non-null) resampled row, you must compute a cryptographic signature by running `/app/data_signer` and passing the string `<timestamp_iso8601>|<sensor_id>|<temperature>` to its standard input. It will output a hex string. Append this signature to the row as a new column `signature`.
4. **Service**: Serve the processed, finalized data via an HTTP API. Your Python application must listen on `127.0.0.1:8080`.
   - Endpoint: `GET /api/data?sensor_id=<id>`
   - Response Format: JSON array of objects, sorted by timestamp ascending. Each object must have keys: `timestamp` (ISO 8601), `sensor_id`, `location` (from metadata), `temperature`, `humidity`, and `signature`.

Run your API server in the background so it remains active. Do not require authentication. Ensure your server can handle simultaneous connections.