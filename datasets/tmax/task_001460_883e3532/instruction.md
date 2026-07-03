You are a data engineer tasked with fixing a broken ETL pipeline for IoT sensor data. The current bash-based pipeline silently drops records that contain embedded newlines in their metadata, leading to inaccurate downstream analytics.

Your task is to write a robust Python script at `/home/user/etl_pipeline.py` that processes the raw time-series data. 

**Source Data:**
- Location: `/home/user/raw_sensor_data.csv`
- Format: CSV with headers `timestamp,sensor_id,temperature,metadata`
- Encoding: `cp1252` (Windows-1252)
- Quirks: The `metadata` column contains free-form text enclosed in double quotes. This text often contains embedded newlines (`\n`) and special characters (like `€`, `ñ`, `°`). 

**Processing Requirements:**
1. **Encoding & Parsing:** Read the CSV correctly, handling the `cp1252` encoding and properly parsing fields with embedded newlines without dropping any rows.
2. **Data Cleaning:** Replace any embedded newlines (`\n` or `\r\n`) within the `metadata` field with a single space (` `).
3. **Filtering:** Drop any rows where the `temperature` is empty or cannot be parsed as a float.
4. **Sorting & Grouping:** Group the records by `sensor_id`. Within each group, sort the records strictly chronologically by `timestamp` (ascending).
5. **Stratified Sampling:** For each `sensor_id` group, retain **only the first 2 chronological readings** where the temperature is strictly greater than `20.0`.
6. **Output:** Write the resulting records to `/home/user/processed_data.jsonl`. Each line must be a valid JSON object with the following schema:
   - `ts`: String (the timestamp)
   - `id`: String (the sensor_id)
   - `temp`: Float (the temperature)
   - `meta`: String (the cleaned metadata)

After writing your script, execute it so that `/home/user/processed_data.jsonl` is generated.