I need you to build a Python-based data processing workflow to handle a stream of sensor readings. 

I have a raw data file at `/home/user/raw_sensors.jsonl`. It is a JSON-lines file where each line is supposed to be a JSON object containing a `timestamp`, `sensor_id`, and a `reading`. However, our upstream data ingestion has a bug: some lines contain malformed unicode escape sequences (like `\uZZZZ` or truncated escapes) which cause standard JSON parsers to crash.

Please write and execute a Python script that performs the following:

1. **Validation Checkpoint (Quality Gate):** Read `/home/user/raw_sensors.jsonl` line by line. Attempt to parse each line as JSON. If a line fails to parse (e.g., due to invalid unicode escapes or formatting), discard it. You must record the 1-based line numbers of all discarded lines by writing them to `/home/user/invalid_lines.txt`, one line number per line.
2. **Normalization:** For each valid JSON line, extract the `reading` field and ensure it is treated as a float.
3. **Windowed Aggregation:** Compute a rolling average of the `reading` values over a sliding window of the last **3 valid records**. 
    * For the first valid record, the average is just its own reading.
    * For the second, it's the average of the first two.
    * For the third and onwards, it's the average of the current reading and the previous two valid readings.
4. **Output:** Write the results for the valid records to a new file at `/home/user/rolling_averages.jsonl`. The output must be in JSON-lines format, where each line is exactly: `{"valid_index": i, "rolling_avg": x}`
    * `i` is the 0-based index of the valid record (i.e., the first valid record is 0, the next is 1, etc.).
    * `x` is the rolling average calculated in step 3, rounded to exactly 2 decimal places.

Ensure your script runs successfully and creates the required output files in `/home/user/`.