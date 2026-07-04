You are an automation specialist for a health-tech company. We receive heart rate monitoring data from various smartwatches and medical devices. Because different devices use different telemetry backends, the raw data arrives in multiple formats (CSV, JSON, and Parquet) with varying column names.

Your task is to build a Python-based data processing pipeline that unifies these files, anonymizes the patient identities, performs anomaly and changepoint detection on the time-series data, and outputs the results.

Here are the requirements:

1. **Input Data:**
   The raw files are located in `/home/user/raw_data/`. There are three files:
   - `device_a.csv` (columns: `date_time`, `patient_id`, `hr`)
   - `device_b.json` (list of objects with keys: `ts`, `uid`, `heart_rate`)
   - `device_c.parquet` (columns: `timestamp`, `user`, `bpm`)

2. **Data Unification & Formatting:**
   - Read all files and combine them into a single dataset.
   - Standardize the columns to exactly: `timestamp`, `user_id`, `value`.
   - Ensure `timestamp` is formatted as a standard ISO 8601 string (e.g., `YYYY-MM-DD HH:MM:SS`) in UTC. If they are already in standard formats, parse and standardize them. Sort the entire combined dataset chronologically by `timestamp`.

3. **Anonymization:**
   - Replace the original `user_id` values with a SHA-256 hash of the original string, prefixed with `"anon_"`. For example, if the user ID is "Alice", the new ID should be `"anon_" + sha256("Alice")`.

4. **Anomaly & Changepoint Detection:**
   Process the time-series data chronologically per user to flag anomalous events. Add a column named `alert_type`.
   - **Anomaly:** A heart rate `value < 40.0` or `value > 150.0`.
   - **Changepoint:** The absolute difference between a user's current `value` and their *immediately preceding* `value` (chronologically) is strictly greater than `30.0`. (The first record for a user cannot be a changepoint).
   - If a record is an anomaly, set `alert_type` to `"anomaly"`.
   - If a record is a changepoint, set `alert_type` to `"changepoint"`.
   - If a record is BOTH, set `alert_type` to `"both"`.
   - Records that trigger neither should drop the `alert_type` column or have it as null (they won't be in the alerts file anyway).

5. **Output Generation:**
   - Create the directory `/home/user/processed/`.
   - Save the fully unified, anonymized, and sorted dataset (ALL records) to `/home/user/processed/unified.parquet`. It should contain columns `timestamp`, `user_id`, `value`.
   - Extract ONLY the records that triggered an alert (anomaly, changepoint, or both). Save this filtered dataset to `/home/user/processed/alerts.json` as a JSON array of objects, sorted by `timestamp` ascending. It must include columns: `timestamp`, `user_id`, `value`, `alert_type`.

Use any Python libraries standard for data processing (like `pandas`, `pyarrow`, or `fastparquet`). You may need to install them using `pip`.