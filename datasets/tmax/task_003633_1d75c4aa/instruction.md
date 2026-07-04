You are tasked with fixing and enhancing a broken ETL data pipeline for a fleet of IoT sensors. 

Currently, our system drops raw sensor logs (CSV format) into `/home/user/data/incoming/`. However, the current scheduled job has been failing and lacks a mechanism to track processed files. This results in the script processing the same files repeatedly on retries, creating duplicate metrics. 

Your objective is to build a robust script in a language of your choice that reads these CSV files, transforms the data, prevents duplicate processing, and outputs the results in multiple formats. You must also schedule this script.

**Pipeline Requirements:**

1. **Input:**
   Read all CSV files present in `/home/user/data/incoming/`.
   The CSV files have the following header: `event_id,timestamp,device_id,sensor_value`.

2. **Deduplication:**
   Deduplicate the incoming records based on the `event_id` column. If multiple records have the same `event_id`, keep only one.

3. **Transformation (Windowed Aggregation):**
   Sort the deduplicated records chronologically by `timestamp` (ascending).
   Calculate a 3-record rolling average of the `sensor_value` for *each* `device_id`. 
   The window should include the current record and the up to 2 immediately preceding records for that specific device. If fewer than 3 records exist for a device up to that point, average the available records. Round the rolling average to 2 decimal places.

4. **Output Formats:**
   Write the final transformed records to two formats simultaneously:
   
   *JSON:* Write to `/home/user/data/output/metrics.json` as a JSON array of objects. Each object must have keys: `event_id`, `timestamp`, `device_id`, `sensor_value`, and `rolling_avg` (as a float).
   
   *XML:* Write to `/home/user/data/output/metrics.xml`. The root element must be `<metrics>`. Each record must be a `<metric>` element containing child elements: `<event_id>`, `<timestamp>`, `<device_id>`, `<sensor_value>`, and `<rolling_avg>`.

5. **State Management:**
   To prevent the "duplicate records on retry" issue, your script must move all successfully processed CSV files from `/home/user/data/incoming/` to `/home/user/data/archive/` at the end of its run.

6. **Scheduling:**
   Install a cron job for the `user` that schedules your script to run every 5 minutes.

**Setup Instructions:**
The directories `/home/user/data/incoming/`, `/home/user/data/output/`, and `/home/user/data/archive/` have been created for you, and some initial CSV files with duplicated data are currently in the `incoming` directory.

Write your script, execute it manually once to process the existing files and ensure the outputs are generated, and set up the cron job.