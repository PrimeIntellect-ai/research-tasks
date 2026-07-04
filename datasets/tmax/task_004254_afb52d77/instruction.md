You need to build a data pipeline to track server configuration changes over time for our infrastructure. The system currently exports configuration change logs in two different formats, and there is a known issue where some legacy CSV logs contain embedded newlines in the message fields that cause silent data dropping in naive pipelines.

You must write a Python script at `/home/user/process_configs.py` that processes these logs and outputs a normalized time-series dataset with rolling statistics.

**Input Data:**
1. `/home/user/data/legacy_configs.csv`
   Columns: `timestamp`, `server_name`, `raw_diff`
   *Note: `raw_diff` contains multiline strings (embedded newlines). Ensure your CSV reader handles this correctly without dropping rows or misaligning columns.*
2. `/home/user/data/modern_configs.json`
   An array of JSON objects with keys: `time`, `host_id`, `changed_keys` (an array of strings).

**Processing Requirements:**
1. **Normalization**:
   - Standardize server names: convert all to lowercase and replace hyphens `-` with underscores `_` (e.g., `SRV-01` and `srv_01` should both become `srv_01`).
   - Standardize timestamps: Parse all timestamps to UTC pandas Datetime objects.
2. **Regex Extraction**:
   - For the CSV data, the `raw_diff` column contains messy text. Extract the names of the configured keys using a regular expression. The keys always appear in the format: `[UPDATE] key_name=` or `[ADD] key_name=`. Extract all matched `key_name`s into a list of strings for that row.
3. **Merge/Union**:
   - Transform both datasets into a common schema: `timestamp` (datetime), `server` (normalized string), `updated_keys` (list of strings), `change_count` (integer, representing the number of keys updated in that event).
   - Union the two datasets into a single DataFrame.
4. **Time Series & Rolling Statistics**:
   - Set the `timestamp` as the index and sort it chronologically.
   - For *each server individually*, compute a 3-hour rolling sum of the `change_count` (closed='right'). Add this as a new column named `rolling_3h_changes`. 
   - Note: Use a time-based rolling window (e.g., `3h` or `3H` in pandas), not an observation-based window.
5. **Output**:
   - Save the final DataFrame as a Parquet file at `/home/user/output/tracked_changes.parquet`.
   - The Parquet file must contain the following columns: `timestamp` (as a column or index), `server`, `change_count`, and `rolling_3h_changes`.

Ensure you install any necessary Python packages (like `pandas`, `pyarrow`, or `fastparquet`) using `pip`.