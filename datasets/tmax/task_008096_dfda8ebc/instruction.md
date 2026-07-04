You are a data analyst responsible for processing time-series IoT sensor data. You have been given a raw CSV file containing sensor readings, but the data pipeline has been failing because some notes fields contain embedded newlines, which naive parsers mishandle. Furthermore, some sensors are malfunctioning and sending out-of-range values.

Your task is to build a robust data processing pipeline consisting of a Python script (`/home/user/pipeline.py`) and a bash orchestrator (`/home/user/run_pipeline.sh`).

**Input Data:**
The raw data is located at `/home/user/sensor_data.csv`.
It has the following columns: `timestamp`, `sensor_id`, `temperature`, `humidity`, `notes`.

**Pipeline Requirements:**
1. **Orchestration (`run_pipeline.sh`):**
   - Create an executable bash script at `/home/user/run_pipeline.sh`.
   - The script must create the directory `/home/user/output/` if it doesn't exist.
   - It must clear any existing files in the `/home/user/output/` directory.
   - Finally, it must execute `/home/user/pipeline.py`.

2. **Data Extraction & Validation (`pipeline.py`):**
   - Read `/home/user/sensor_data.csv`, properly handling embedded newlines in the `notes` column (do not drop these rows).
   - Validate each row using the following constraints:
     - `temperature` must be a valid float between `-20.0` and `60.0` (inclusive).
     - `humidity` must be a valid float between `0.0` and `100.0` (inclusive).
   - Rows that **fail** these validation constraints must be written exactly as they appeared (with all original columns and formatting) to `/home/user/output/invalid_rows.csv`. Include the CSV header in this file.

3. **Time Series Aggregation:**
   - For the **valid** rows, group the data by `sensor_id`.
   - Ensure the records for each sensor are processed in chronological order based on `timestamp`.
   - Calculate a trailing 3-row moving average for both `temperature` and `humidity`.
     - The moving average for a given row should include that row and up to 2 previous valid rows for the same sensor. (If it's the first valid reading for a sensor, the average is just that reading's value. If it's the second, it's the average of the first and second).

4. **Output Generation:**
   - Write the aggregated results for the valid rows to a JSON Lines file at `/home/user/output/rolling_stats.jsonl`.
   - Each line should be a JSON object with the following keys exactly: `timestamp`, `sensor_id`, `temp_mavg`, `hum_mavg`.
   - The moving average values (`temp_mavg` and `hum_mavg`) must be floats rounded to exactly 2 decimal places.
   - The output must be ordered chronologically by `timestamp` across all sensors. If timestamps are identical, preserve the original order from the input file.

Ensure you make `/home/user/run_pipeline.sh` executable and run it to produce the final output files.