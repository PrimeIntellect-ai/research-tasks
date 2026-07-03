You are an AI assistant helping a data scientist clean and prepare a dataset from various IoT sensors. 

You have been given a directory `/home/user/sensor_data` containing raw sensor logs in different formats (CSV and JSON). The files contain records with duplicate entries, misaligned timestamps, and raw metrics that need feature extraction.

Your task is to write a Python script (you can place it anywhere, e.g., `/home/user/clean.py`) that reads all files in the `/home/user/sensor_data` directory and performs the following operations:

1. **Timestamp Alignment**: 
   - Extract the `timestamp` field.
   - For CSV files, the timestamps are strings in either `YYYY/MM/DD HH:MM:SS` or `DD-MM-YYYY HH:MM:SS` formats. Assume they are in UTC.
   - For JSON files, the timestamps are integers representing epoch time in milliseconds.
   - Convert all timestamps to standard ISO 8601 format with a 'Z' indicating UTC (e.g., `2023-10-01T12:00:00Z`).

2. **Feature Extraction**:
   - Each record contains `temperature` and `humidity` as numeric values.
   - Calculate a derived feature called `heat_index` using the simplified formula: `heat_index = temperature + (0.5 * humidity)`.
   - Round the `heat_index` to exactly 2 decimal places.

3. **Hash-based Deduplication**:
   - Combine data from all files.
   - Deduplicate the records across the entire dataset. A record is considered a duplicate if it has the exact same `sensor_id`, ISO 8601 `timestamp`, `temperature`, and `humidity`. 
   - Keep only one instance of any duplicate record.

4. **Output formatting**:
   - Write the final cleaned and feature-enhanced dataset to a single JSON Lines (JSONL) file at `/home/user/cleaned_data.jsonl`.
   - Each line should be a JSON object with the following keys exactly: `sensor_id`, `timestamp`, `temperature`, `humidity`, `heat_index`.
   - The records in the output file must be sorted alphabetically by `sensor_id`, and then chronologically by `timestamp`.

Ensure you run your script and verify that `/home/user/cleaned_data.jsonl` is created correctly.