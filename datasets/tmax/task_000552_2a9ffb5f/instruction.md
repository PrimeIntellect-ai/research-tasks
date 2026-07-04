You are an AI assistant helping a data scientist clean and process smart factory data. You need to build a multi-stage data processing pipeline in Python.

The working directory is `/home/user/factory_data`. You will find two input files there:
1. `maintenance_logs.txt`: Unstructured technician logs.
2. `sensor_telemetry.csv`: Hourly sensor readings.

Your objective is to write Python scripts to orchestrate a data pipeline that does the following:

**Phase 1: Information Extraction**
Write a script `extract.py` that reads `maintenance_logs.txt` and extracts structured data.
Each line in the text file contains an implicit record. You need to extract:
- `timestamp`: The date and time (format: YYYY-MM-DD HH:MM:SS) at the beginning of the line.
- `machine_id`: The identifier starting with "Mach-" (e.g., Mach-101, Mach-204).
- `error_code`: The code immediately following "ErrCode:" (e.g., E44, E99).
- `downtime_minutes`: The integer value immediately preceding "minutes downtime".

Save this extracted data to `/home/user/factory_data/extracted_logs.csv` with columns: `timestamp,machine_id,error_code,downtime_minutes`.

**Phase 2: Joins and Rolling Statistics**
Write a script `process.py` that reads `extracted_logs.csv` and `sensor_telemetry.csv`.
For every maintenance event in `extracted_logs.csv`, compute the rolling average of the `temperature` and `vibration` sensors for that specific `machine_id` over the **3-hour window strictly before** the event's timestamp. 
Specifically, include sensor readings where `event_timestamp - 3 hours <= sensor_timestamp < event_timestamp`.

If there are no sensor readings in that window for that machine, output `null` for the averages.

**Phase 3: Output**
The `process.py` script should output a JSON Lines file at `/home/user/factory_data/final_metrics.jsonl`.
Each line should be a JSON object representing a maintenance event, with the following keys exactly:
- `event_timestamp` (string: "YYYY-MM-DD HH:MM:SS")
- `machine_id` (string)
- `error_code` (string)
- `downtime_minutes` (integer)
- `avg_temperature` (float, rounded to 2 decimal places, or null)
- `avg_vibration` (float, rounded to 2 decimal places, or null)

**Phase 4: Orchestration**
Write a bash script `run_pipeline.sh` in `/home/user/factory_data` that runs `extract.py` followed by `process.py`. Ensure the script is executable.

You may install and use `pandas` if desired.