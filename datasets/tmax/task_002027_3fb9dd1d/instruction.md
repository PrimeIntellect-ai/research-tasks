You are tasked with building a highly performant mathematical data processing pipeline for a continuous stream of sensor data. 

There are two main phases to this task: fixing the local parallel processing environment and implementing the processing script.

**Phase 1: Environment Setup**
We heavily rely on the `joblib` package for parallel processing. A specific version of its source code has been vendored at `/app/joblib-1.3.2`. However, it currently fails to install due to a deliberate configuration perturbation (a typo in its dependency list).
1. Navigate to `/app/joblib-1.3.2`.
2. Find and fix the typo in its packaging configuration that is preventing installation (hint: look at the required packages).
3. Install the package into the system environment (e.g., `pip install -e .`).

**Phase 2: The Processing Pipeline**
Create a Python script at `/home/user/analyze.py`. 
This script must read standard wide-format CSV data from `stdin` and print the processed output to `stdout`.

**Input Format (stdin):**
A CSV with the following columns: `timestamp, sensor_id, metric_a, metric_b, metric_c`
Example row: `1690000000, sens_01, 10.5, 20.1, 5.0`

**Processing Requirements:**
1. **Wide-to-Long Reshaping:** Convert the `metric_a`, `metric_b`, and `metric_c` columns into a long format. The new columns should be `variable` (containing the metric name) and `value`.
2. **Parallel Processing:** You MUST use the newly installed `joblib.Parallel` to parallelize the next step. Group the data by `sensor_id`, and dispatch the processing of each unique `sensor_id` to a separate worker.
3. **Rolling Statistics:** For each `sensor_id` and `variable` combination, sort the records strictly by `timestamp` (ascending). Calculate a rolling Simple Moving Average (SMA) of the `value` using a window size of exactly `3`. 
   - For the first 2 chronological records of any group (where a full 3-window is impossible), the moving average should be rendered as an empty string (i.e., nothing between the commas).
   - Format the calculated rolling average strictly to 2 decimal places (e.g., `15.20`).

**Output Format (stdout):**
The script must print a valid CSV with a header row: `timestamp,sensor_id,variable,value,rolling_avg`.
Rows must be sorted primarily by `sensor_id` (ascending, alphabetical), then by `variable` (ascending, alphabetical), and finally by `timestamp` (ascending, numerical).

Example Output:
```csv
timestamp,sensor_id,variable,value,rolling_avg
1690000000,sens_01,metric_a,10.5,
1690000010,sens_01,metric_a,11.0,
1690000020,sens_01,metric_a,11.5,11.00
...
```

Make sure the script is robust, strictly matches the requested formatting, handles arbitrary lengths of stdin, and gracefully uses the patched `joblib`.