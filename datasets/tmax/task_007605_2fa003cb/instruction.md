You are a data scientist working in a manufacturing plant. You have been tasked with cleaning and analyzing temperature sensor data from 20 different machines. The data has been extracted into individual CSV files.

You need to write and execute a Python script to process these files, identify anomalous machines, and log the pipeline execution.

**Input Data:**
- Reference time series: `/home/user/reference.csv`
- Sensor data directory: `/home/user/sensor_data/` containing 20 files named `machine_01.csv` through `machine_20.csv`.
- Each CSV has two columns: `timestamp` (integer from 0 to 999) and `temperature` (float). All files have exactly 1000 rows with matching timestamps.

**Requirements for your Python script (`/home/user/clean_sensors.py`):**
1. **Parallel Processing:** You must use Python's `multiprocessing` or `concurrent.futures` module to process the 20 machine files in parallel.
2. **Distance Computation:** For each machine, calculate the Euclidean distance between its `temperature` array and the `temperature` array of `reference.csv`.
3. **Changepoint/Anomaly Detection:** For each machine, calculate the rolling standard deviation of its `temperature` array using a window size of 50. If the maximum rolling standard deviation is strictly greater than `2.5`, flag the machine as having a changepoint.
4. **Anomaly Rules:** A machine is considered "anomalous" if EITHER:
   - Its Euclidean distance to the reference is strictly greater than `100.0`
   - It is flagged as having a changepoint (max rolling std dev > 2.5).
5. **Logging:** You must implement pipeline logging using Python's `logging` module. Configure it to write to `/home/user/pipeline.log`.
   - Format: `%(asctime)s - %(levelname)s - Processed %(filename)s - Distance: %(distance).2f - Changepoint: %(changepoint)s` (where filename is just the basename like `machine_01.csv`).
   - Log at the `INFO` level for each processed file.
6. **Output:** The script must write a JSON file to `/home/user/anomalies.json` containing a simple list of the filenames (just the basenames, e.g., `["machine_03.csv", "machine_15.csv"]`) that were determined to be anomalous. The list must be sorted alphabetically.

Write the script, run it, and ensure the log file and JSON output are generated correctly. You may install standard data science packages like `pandas` or `numpy` if needed using `pip`.