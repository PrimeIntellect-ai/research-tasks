You are a data engineer tasked with building an ETL pipeline to process telemetry logs from a fleet of delivery trucks. The sensors log temperature and GPS coordinates, but the raw data is messy due to legacy firmware issues.

You have been provided a raw log file at `/home/user/raw_data.log`.

Your objective is to create a robust, multi-language data pipeline that cleans, normalizes, resamples, and imputes this time-series data. 

Here are the requirements:

1. **Pipeline Orchestration (Bash)**:
   Write a Bash script at `/home/user/run_etl.sh`. This script should:
   - Make sure any required system or Python packages (e.g., `pandas`) are installed (assume a Debian/Ubuntu-based environment where you can use pip).
   - Pre-process `/home/user/raw_data.log` using standard Unix text-processing tools (`grep`, `sed`, or `awk`) to filter out any log lines that contain the substring `Status:ERROR` or `Status:FAIL`. Save this intermediate file to `/home/user/filtered_data.log`.
   - Execute a Python script (which you must also write) to perform the advanced time-series transformations on the filtered data.

2. **Data Transformation (Python)**:
   Write a Python script at `/home/user/process.py` that reads `/home/user/filtered_data.log` and performs the following:
   - **Regex Parsing**: Extract the Truck ID (e.g., `TRK-001`), the Timestamp, and the Temperature value (in Celsius). 
     *Note: The timestamps in the log appear in two different formats due to a firmware bug: ISO8601 (`YYYY-MM-DDTHH:MM:SSZ`) and US format (`MM/DD/YYYY HH:MM:SS`). Your regex and parsing logic must handle both and normalize them to a standard datetime object.*
   - **Sorting & Grouping**: Sort the dataset chronologically and group the records by Truck ID.
   - **Resampling & Gap-filling**: The sensors are supposed to report exactly every 5 minutes (aligned to the minute, e.g., 10:00:00, 10:05:00), but network drops cause missing records. For each Truck ID, resample the time series to a strict 5-minute frequency, spanning from that truck's first valid timestamp to its last valid timestamp.
   - **Imputation**: For any newly created timestamps resulting from the 5-minute resampling, fill in the missing temperature values using **linear interpolation** based on the surrounding valid data points.

3. **Output Specification**:
   The Python script must save the final processed data to `/home/user/processed.csv`.
   - The CSV must have exactly three columns in this order: `truck_id`, `timestamp`, `temperature`.
   - `timestamp` must be formatted strictly as `YYYY-MM-DD HH:MM:SS`.
   - `temperature` must be rounded to exactly 2 decimal places (e.g., `12.00`, `14.50`).
   - Include a header row.
   - Sort the output first by `truck_id` (ascending) and then by `timestamp` (ascending).

To complete the task, ensure both your scripts (`run_etl.sh` and `process.py`) are fully functional, and execute `/home/user/run_etl.sh` so that the final `/home/user/processed.csv` file is generated.