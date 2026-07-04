You are an AI assistant helping a configuration manager analyze server configuration changes over time. We have collected a log of configuration states from various servers, but the data is irregular, contains duplicate texts, and is too large to analyze at once.

Your task is to write a Python script that processes this data and produces a standardized, sampled daily timeline report.

Here are the requirements:

1. **Input Data**: A CSV file is located at `/home/user/config_history.csv` with the following columns:
   `timestamp,server_name,environment,config_text`
   (Timestamps are in ISO 8601 format, e.g., `2023-10-01T14:30:00Z`).

2. **Hash-Based Deduplication**: 
   The `config_text` can be long. Replace the `config_text` column with a `config_hash` column. The `config_hash` must be the **MD5 hexadecimal digest** of the exact `config_text` string.

3. **Resampling and Gap-Filling**:
   - We need a regular daily timeline for each server from exactly `2023-10-01` to `2023-10-07` (inclusive). 
   - Convert the `timestamp` to a date string (`YYYY-MM-DD`). 
   - If a server has multiple configuration logs on the same date, keep only the *chronologically last* one for that day.
   - For any missing dates in the `2023-10-01` to `2023-10-07` range, **forward-fill** the `config_hash` from the previous day. 
   - If a server has no known configuration on or before a given date in this range, fill the hash as the exact string `"NO_CONFIG"`.

4. **Data Sampling and Stratification**:
   - We only want to analyze a representative sample of servers to save processing time downstream.
   - Perform deterministic stratified sampling: For each unique `environment`, select exactly the **first 2 servers** when sorted alphabetically by `server_name`. If an environment has fewer than 2 servers, include all of them.
   - Filter your resampled timeline to only include these sampled servers.

5. **Output**:
   Save the final processed dataset to `/home/user/stratified_config_timeline.csv`.
   The output CSV must have exactly these columns:
   `date,server_name,environment,config_hash`
   Sort the final CSV by `environment` (ascending), `server_name` (ascending), and `date` (ascending).

Write and execute a Python script to perform this data processing. Ensure the final file exists and is correctly formatted.