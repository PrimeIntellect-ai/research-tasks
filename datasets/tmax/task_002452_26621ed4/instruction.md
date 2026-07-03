You are an automation specialist tasked with building a lightweight data processing pipeline. We have a noisy log file from our IoT temperature sensors located at `/home/user/raw_sensors.log`. 

Your goal is to write a Python script at `/home/user/pipeline.py` that processes this log file and deposits the cleaned data into a simulated remote directory.

The pipeline must perform the following tasks in order:
1. **Extraction & Deduplication**: 
   - Read `/home/user/raw_sensors.log`.
   - The log lines follow this format: `LOG_START [{timestamp}] - {sensor_id} reported temp: {value}`
   - Extract the `timestamp`, `sensor_id`, and `temperature` (`value`).
   - Deduplicate the entries: Compute an MD5 hash of the *exact raw log line* (including whitespace). If multiple lines have the same MD5 hash, keep only the first occurrence.
2. **Imputation**:
   - Some temperature values failed to record and appear as `ERROR`. 
   - Parse the extracted data into a structured format (e.g., using `pandas`).
   - For each `sensor_id` independently, perform a **linear interpolation** to fill in the missing temperature values based on the time sequence.
3. **Transfer**:
   - Save the final cleaned data as a CSV file.
   - The CSV must have exactly these columns: `timestamp,sensor_id,temperature`
   - Sort the CSV first by `timestamp` (ascending), then by `sensor_id` (ascending).
   - Format the temperature to 1 decimal place.
   - Transfer (copy/move) this final CSV to `/home/user/remote_archive/cleaned_data.csv`.

Create any necessary directories. You may install and use `pandas` if desired. Run your pipeline so that `/home/user/remote_archive/cleaned_data.csv` is generated successfully.