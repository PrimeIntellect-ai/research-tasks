You are a data engineer building a lightweight ETL pipeline to process time-series sensor data.

We have a raw sensor dataset located at `/home/user/raw_sensors.csv`. The system generating this file is legacy and encodes the CSV in **ISO-8859-1**. The file has a header and three columns: `timestamp` (YYYY-MM-DD HH:MM:SS), `sensor_name`, and `temperature`.

Your task is to create a Go script `/home/user/etl.go` that performs the following pipeline steps:
1. **Read & Decode:** Read `/home/user/raw_sensors.csv` and convert the `sensor_name` field from ISO-8859-1 to UTF-8. 
2. **Constraint-based Validation:** Drop any rows where the temperature is strictly less than `-50.0` or strictly greater than `150.0`. Skip the header row.
3. **Sampling:** We only want one reading per hour. For each distinct hour (e.g., `2023-10-01 10:00:00` to `10:59:59`), keep ONLY the chronologically *first* valid reading found in the file.
4. **Data Load:** Append the resulting sampled records to `/home/user/processed_sensors.csv` in standard UTF-8. Format: `timestamp,sensor_name,temperature` (no header).
5. **Logging:** Append a single log line to `/home/user/etl.log` upon completion in this exact format: `SUCCESS: Extracted <N> samples.` (where `<N>` is the number of rows written).

After you write and successfully test the Go script, set up a cron job for the current user (`user`) that schedules this pipeline to run every 15 minutes. The cron command must execute: `/usr/local/go/bin/go run /home/user/etl.go`

Please execute the script once manually so the output files are generated for verification.