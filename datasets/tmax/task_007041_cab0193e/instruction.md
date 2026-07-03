You are tasked with building a robust data processing pipeline to track historical configuration changes across our infrastructure. 

We have a set of configuration exports in `/home/user/config_exports/` stored as a mix of CSV and JSON files. Previous attempts to process this data used naive line-by-line reading, which silently dropped or corrupted rows because some CSV fields contain embedded newlines.

You need to write a Python script `/home/user/process_configs.py` to process these files and generate a deduplicated, daily summary of configuration states. 

Here are the requirements for your pipeline:

1. **Input Ingestion**: 
   - Read all `.csv` and `.json` files in `/home/user/config_exports/`.
   - CSVs have the headers: `timestamp`, `server_id`, `config_a`, `config_b`, `config_c`, `description`.
   - JSONs contain records with the structure: `{"timestamp": "...", "server_id": "...", "configs": {"config_a": "...", "config_b": "...", "config_c": "..."}, "description": "..."}`.
   - You must correctly parse CSVs, accounting for embedded newlines in the `description` field.

2. **Validation Checkpoint**:
   - Any record missing a `timestamp` or `server_id` (either null, empty string, or absent) must be dropped.
   - Write the exact total number of dropped records across all files to `/home/user/output/validation.txt` in the format: `Dropped count: X` (where X is the integer count).

3. **Wide-to-Long Reshaping & Hashing**:
   - For valid records, extract the configuration parameters (`config_a`, `config_b`, `config_c`). Ignore keys that are empty, null, or absent.
   - Sort the remaining configuration keys alphabetically.
   - Format them as a single string like `key1:value1|key2:value2`.
   - Compute the SHA-256 hash (hex digest) of this string to serve as the `state_hash`. If a server has no valid configurations, the hash should be of an empty string.

4. **Time-Based Bucketing & Deduplication**:
   - Extract the `date` (YYYY-MM-DD) from the `timestamp` (which is in ISO 8601 format, e.g., `2023-10-01T14:30:00Z`).
   - Group records by `date` and `server_id`.
   - Within each day and server, deduplicate the states so that only unique `state_hash` values remain.

5. **Output**:
   - Ensure the directory `/home/user/output/` exists.
   - Write the deduplicated results to `/home/user/output/daily_configs.csv` with the headers: `date,server_id,state_hash`.
   - Sort the output rows primarily by `date` (ascending), then by `server_id` (ascending), and finally by `state_hash` (ascending).

Write and execute your script to produce the output files.