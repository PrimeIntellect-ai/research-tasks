You are a data scientist tasked with modernizing a data ingestion pipeline. We currently receive high-frequency sensor telemetry from a local TCP stream, but the data is noisy, contains gaps, and includes redundant back-to-back readings. 

We used to process this with a legacy binary (`/app/legacy_cleaner`), but we lost the source code and need a new, highly performant implementation in Go.

Your objectives:

1. **Re-implement the Data Cleaner in Go**
Create a Go program at `/home/user/cleaner.go` and compile it to `/home/user/cleaner`.
The program must read CSV lines from standard input (`stdin`) and write JSON Lines to standard output (`stdout`). 
Input format: `timestamp_sec,sensor_id,value` (e.g., `1700000000,TEMP_1,42`).
    * **Hash-based Deduplication:** Calculate the SHA-256 hash of the string `<sensor_id>:<value>`. If this hash exactly matches the hash of the *immediately preceding* valid record (across the whole stream), silently drop the current record.
    * **Gap-filling:** Keep track of the last seen `timestamp_sec` (globally, across all sensors). If a new valid record's timestamp is strictly greater than `last_timestamp + 10`, you must emit synthetic records before emitting the new record. Emit a synthetic record at `last_timestamp + 10`, `last_timestamp + 20`, etc., until the next synthetic record would be $\ge$ the new record's timestamp. Synthetic records always have `sensor_id` = `"FILL"` and `value` = `0`.
    * **Streaming Output:** For every valid record (and synthetic record), emit a JSON object on a new line: `{"t": timestamp, "s": "sensor_id", "v": value}`.
    * **Summary Aggregation:** Maintain a running sum of all `value`s emitted. Upon reaching EOF on stdin, emit one final JSON line: `{"total_records": N, "sum": S}`, where N is the total number of emitted JSON lines (excluding this summary) and S is the sum of their values.

2. **Establish the Pipeline**
There is a raw data stream server running locally on TCP port `8080`, and a Redis server on port `6379`.
Create a bash script `/home/user/pipeline.sh` that:
    - Uses `nc localhost 8080` to read exactly 500 lines of data.
    - Pipes that data through your compiled `/home/user/cleaner`.
    - Pipes the JSON output to a command that pushes each line to a Redis list named `sensor_data_cleaned` (using `redis-cli`).

3. **Scheduling**
Configure a user cron job for the `user` account to run `/home/user/pipeline.sh` every minute.

Ensure your Go binary perfectly matches the logic described above, as it will be rigorously fuzzed against the expected output format using diverse edge cases!