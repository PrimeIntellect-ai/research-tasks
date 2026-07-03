You are tasked with processing a log of server configuration changes to prepare it for analysis. A raw data file is located at `/home/user/config_changes.jsonl`. This file contains periodic (but irregular) reports of server metrics and configurations.

Your goal is to write a Python script that processes this data and produces two output CSV files. 

Here are the requirements for the processing:
1. **Resampling and Gap-filling**: 
   - Group the data by `server_id`.
   - The timestamps are irregular. You must resample the time series for each server to a strict 1-hour frequency, starting from the minimum timestamp and ending at the maximum timestamp for that specific `server_id`.
   - For any newly created timestamps (gaps), forward-fill the `config_val` and `role` fields from the most recent previous record. 
   - If a server's first record is missing in the resampled period, backward-fill it.

2. **Data Masking and Anonymization**:
   - The `ip_address` field contains sensitive internal IPs. Mask all IP addresses in the dataset by replacing the last octet with `XXX` (e.g., `192.168.1.50` becomes `192.168.1.XXX`). Do this for all rows in the resampled dataset.

3. **Stratified Sampling**:
   - After creating the full cleaned dataset, create a 25% stratified random sample based on the `role` column. Use a random seed of `42` for the sampling process to ensure reproducibility.
   - The sample should retain the exact same columns.

Output requirements:
- Save the fully resampled, gap-filled, and masked dataset to `/home/user/processed_full.csv`.
- Save the 25% stratified sample to `/home/user/sampled_configs.csv`.
- Both CSV files should contain the columns: `timestamp`, `server_id`, `role`, `ip_address`, `config_val`. 
- The `timestamp` column should be formatted as an ISO 8601 string (e.g., `2023-10-01T12:00:00`).
- Ensure the output CSVs do not contain an index column.

You may install any Python libraries you need (e.g., pandas) using pip.