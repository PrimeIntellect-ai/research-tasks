You are a data engineer building a streaming ETL pipeline for a multi-lingual IoT sensor network. You need to accomplish two main phases:

**Phase 1: Parameter Extraction from Audio**
We have intercepted a voice memo from the lead engineer detailing the latest timezone offset and threshold configurations, located at `/app/audio/config_memo.wav`. 
You must transcribe this audio file. The audio contains a spoken instruction in English and Spanish that specifies:
1. The integer time-shift offset (in minutes) to apply to all incoming sensor timestamps.
2. The exact Unicode string of the target location we are monitoring.

**Phase 2: Build the Stream Processor**
You must write a Python script at `/home/user/stream_processor.py` that processes incoming real-time sensor logs from standard input (`stdin`) and outputs aggregated statistics to standard output (`stdout`).

Your script must do the following:
1. **Load Reference Data**: Read the reference catalog located at `/app/data/sensor_catalog.csv`. This file contains metadata for each sensor (sensor_id, location_name, base_threshold). Note: The system that generated this catalog is legacy and outputs in `UTF-16LE` encoding with multi-language (Unicode) characters.
2. **Process `stdin` Stream**: Read JSON-formatted strings line by line from `stdin`. Each line represents a sensor reading: `{"timestamp": "2023-10-25T14:32:15Z", "sensor_id": "A1B", "value": 45.2, "status": "OK"}`.
3. **Data Transformation**:
   - Parse the ISO-8601 timestamps.
   - Apply the time-shift offset (in minutes) recovered from the audio file in Phase 1 to the timestamps.
   - Truncate/bucket the adjusted time into strictly **15-minute intervals** (e.g., 14:00:00, 14:15:00).
4. **Join & Filter**: Join the incoming stream with the reference data using `sensor_id`. Filter the resulting dataset so that you *only* process records matching the exact Unicode location string recovered from the audio file.
5. **Aggregation**: For each 15-minute bucket and `sensor_id` combination, calculate summary statistics:
   - `reading_count` (integer)
   - `mean_value` (float, rounded to 2 decimal places)
   - `max_value` (float, rounded to 2 decimal places)
6. **Output**: Print the aggregated results to `stdout` as a JSON array of objects, sorted chronologically by the bucketed timestamp, then alphabetically by `sensor_id`. Each object must look like: 
   `{"bucket": "2023-10-25T14:15:00Z", "sensor_id": "A1B", "reading_count": 5, "mean_value": 44.12, "max_value": 48.5}`

Your script must perfectly match our reference implementation. An automated test will supply thousands of synthetic, fuzzed JSON logs to your script via `stdin` and compare the exact `stdout` bytes against our oracle binary.