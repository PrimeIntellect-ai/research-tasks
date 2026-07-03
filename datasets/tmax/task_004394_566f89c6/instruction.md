You are tasked with building a data processing pipeline to track and analyze configuration file changes across a simulated server fleet. We have raw metrics containing timestamps, server IDs, configuration file sizes, and the number of changes made. This data is irregular and contains gaps.

Your goal is to build an automated pipeline using a `Makefile` (DAG orchestration) and a combination of languages (e.g., Python and Bash) to process this data, resample it, calculate rolling statistics, and detect anomalies.

**Input Data:**
The raw data is located at `/home/user/raw_config_metrics.csv`.
Columns: `timestamp` (ISO8601, e.g., 2023-10-01T14:32:00Z), `server_id` (string), `config_size_bytes` (integer), `changes_count` (integer).

**Pipeline Requirements:**

1. **Resampling and Gap-Filling**:
   - Aggregate the data to a **daily** frequency (using the date part of the timestamp in UTC) for each `server_id`.
   - If there are multiple records for a server on a single day, take the **last** `config_size_bytes` of the day, and the **sum** of `changes_count`.
   - **Gap-filling**: For days where a server has no data, fill the missing days. The date range for each server should be from its first appearance in the dataset to its last appearance.
   - For missing days, forward-fill (carry forward) the previous day's `config_size_bytes`.
   - For missing days, fill `changes_count` with `0`.

2. **Windowed Aggregation**:
   - For each server, calculate a **7-day rolling average** of `config_size_bytes` (inclusive of the current day and the 6 preceding days).
   - Calculate the **7-day rolling standard deviation** (sample standard deviation) of `config_size_bytes`. Use a minimum of 3 days of data (if fewer than 3 days are available in the window, output null/NaN for the standard deviation).

3. **Anomaly Detection**:
   - A day is flagged as an anomaly (`is_anomaly = true`) if the `config_size_bytes` for that day deviates from the 7-day rolling average by strictly more than **2.0 times the 7-day rolling standard deviation**.
   - If the standard deviation is null/NaN (due to insufficient history) or 0, it is NOT an anomaly.

4. **Orchestration**:
   - Create a `Makefile` at `/home/user/Makefile` with a default `all` target.
   - Running `make` should process the raw data and produce the final output file `/home/user/detected_anomalies.json`.

**Final Output Format:**
The output `/home/user/detected_anomalies.json` must be a JSON array of objects, containing **ONLY** the records flagged as anomalies, sorted chronologically by date, then alphabetically by server_id.

Each object must match this schema exactly:
```json
[
  {
    "date": "2023-10-05",
    "server_id": "srv-alpha",
    "config_size_bytes": 15000,
    "rolling_mean": 12000.5,
    "rolling_std": 1450.2,
    "is_anomaly": true
  }
]
```
*(Note: Round `rolling_mean` and `rolling_std` to 1 decimal place in the final JSON).*

You may install any necessary libraries (e.g., pandas) in your local user environment (`pip install --user`). Do not use root privileges.