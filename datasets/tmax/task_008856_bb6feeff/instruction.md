You are an automation specialist setting up a data processing workflow for an IoT sensor network. The raw telemetry data arrives in a JSONL (JSON Lines) format, but network retries often cause exact duplicate events to be logged. 

You need to write a Python script at `/home/user/process_telemetry.py` that processes this data and produces both summary statistics and a pipeline execution log.

Here are your detailed requirements:

1. **Input Data**: 
   The raw data is located at `/home/user/incoming/telemetry.jsonl`. Each line is a JSON object with three keys: `sensor_id` (string), `timestamp` (string), and `value` (float).

2. **Hash-Based Deduplication**:
   Read the file line by line. Deduplicate the events by generating an MD5 hash of a composite string formatted exactly as `"{sensor_id}|{timestamp}"`. Keep only the first occurrence of each hash. Ignore and drop any subsequent records that produce the same MD5 hash.

3. **Summary Statistics**:
   Calculate the average `value` for each unique `sensor_id` based *only* on the deduplicated records. Round the average to exactly 2 decimal places. 
   Save this aggregated data to `/home/user/output/averages.json` as a single JSON object where keys are the `sensor_id`s and values are the calculated averages.

4. **Pipeline Logging**:
   To monitor the workflow, save a pipeline execution summary to `/home/user/logs/pipeline_stats.json`. This must be a JSON object containing exactly these three integer keys:
   - `"total_records_read"`: The total number of lines read from the input file.
   - `"duplicates_dropped"`: The number of duplicate records ignored based on the MD5 hash.
   - `"unique_sensors_found"`: The total number of distinct `sensor_id`s present in the deduplicated data.

Ensure your script creates the necessary output directories (`/home/user/output` and `/home/user/logs`) if they do not exist. Run your script to generate the final files.