You are tasked with building a robust bash-based ETL pipeline to process configuration change logs. 

A configuration management system has been logging changes to various system parameters over time, but the logging mechanism is flawed. The logs contain duplicate entries, irregular time intervals, and inconsistent formatting. 

Your objective is to write a bash script (using standard CLI tools like `awk`, `sed`, `sort`, etc.) to clean, normalize, impute, and extract features from this time-series data.

**Input Data:**
A messy log file located at `/home/user/raw_config.csv`. 
The file has no header. It contains three comma-separated columns:
`timestamp, param_name, value`

**Processing Requirements:**

1. **Filtering & Normalization**: 
   - Trim any leading/trailing whitespace from all fields.
   - Convert `param_name` to strictly lowercase.
   - We are *only* interested in the parameter named `max_workers`. Completely ignore all rows pertaining to other parameters.

2. **Deduplication / Conflict Resolution**:
   - There may be multiple `max_workers` entries for the exact same timestamp. 
   - When conflicts occur for the same timestamp, you must keep only the entry with the **maximum** `value`.

3. **Interpolation / Imputation**:
   - The configuration system requires a strictly regular time series with a step size of **10 seconds**.
   - Determine the minimum timestamp and maximum timestamp among the valid `max_workers` records.
   - Generate a continuous sequence of timestamps from the minimum to the maximum in steps of 10.
   - If a timestamp is missing from the logged data, impute the `value` using **forward fill** (Last Observation Carried Forward - use the value from the most recent previous timestamp). 

4. **Feature Extraction**:
   - Calculate a new metric: `delta`.
   - `delta` is the difference between the current row's `value` and the previous row's `value` (`current - previous`).
   - For the very first row in the time series, `delta` must be `0`.

**Output Specification:**
Create your final processed dataset at `/home/user/clean_config.csv`.
- The output file **must** contain a header row: `timestamp,param_name,value,delta`
- The file must be sorted chronologically by `timestamp`.
- The `param_name` in the output should always be `max_workers`.

**Constraints:**
- You must use Bash and standard Linux command-line utilities (e.g., `awk`, `grep`, `sort`, `sed`, `join`). Do not use Python, Perl, or any non-standard data processing binaries.
- Ensure your script is completely self-contained and runs without user intervention.